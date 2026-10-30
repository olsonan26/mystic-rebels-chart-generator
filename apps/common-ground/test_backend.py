"""Meaningful calculation, civil-time and API boundary checks for the local adapter."""
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True

from fastapi.testclient import TestClient

from app import app, ComparisonInput
from numerology import calculate_numerology, reduce_with_chain

client = TestClient(app)


def generic_input(**changes):
    value = {
        "full_name": "Avery Morgan", "birth_date": "1988-01-15",
        "birth_time": "12:00", "time_accuracy": "nearest_minute",
        "latitude": 33.80279, "longitude": -118.06201,
        "timezone": "America/Los_Angeles", "location_name": "Test city centroid",
    }
    return {**value, **changes}


class NumerologyChecks(unittest.TestCase):
    def test_master_chains_and_zero_are_literal(self):
        self.assertEqual(reduce_with_chain(74)["sequence"], [74, 11])
        self.assertEqual(reduce_with_chain(49)["sequence"], [49, 13, 4])
        self.assertEqual(reduce_with_chain(33)["value"], 33)
        self.assertEqual(reduce_with_chain(0)["value"], 0)

    def test_date_component_and_birth_force_are_distinct_methods(self):
        result = calculate_numerology("AAAA", "1980-11-11")
        core = {row["role"]: row for row in result["core_numbers"]}
        self.assertEqual(core["Birth Force"]["value"], 22)
        self.assertEqual(core["Ultimate Goal"]["birthday_component"]["value"], 4)
        self.assertEqual(core["Ultimate Goal"]["value"], 8)

    def test_middle_names_affect_expression_but_not_called_role(self):
        first = calculate_numerology("KA H", "1988-01-15")
        second = calculate_numerology("KA Test H", "1988-01-15")
        a = {row["role"]: row for row in first["core_numbers"]}
        b = {row["role"]: row for row in second["core_numbers"]}
        self.assertNotEqual(a["Expression"]["raw"], b["Expression"]["raw"])
        self.assertEqual(a["Called Name"]["value"], 11)
        self.assertEqual(b["Called Name"]["value"], 11)

    def test_pmei_counts_are_not_sums_or_reduced_digits(self):
        result = calculate_numerology("AAAAAAAAAAA", "1988-01-15")
        self.assertEqual(result["planes"]["mental"]["count"], 11)
        self.assertEqual(result["total_letters"], 11)
        self.assertEqual(sum(row["count"] for row in result["planes"].values()), 11)
        self.assertEqual(result["zero_planes"], ["physical", "emotional", "intuitive"])
        self.assertTrue(result["pmei"]["qa_checksum_passed"])

    def test_no_vowel_is_not_silently_nine(self):
        result = calculate_numerology("Y", "1988-01-15")
        soul = next(row for row in result["core_numbers"] if row["role"] == "Soul Urge")
        self.assertEqual(soul["value"], 0)
        self.assertTrue(result["warnings"])

    def test_pmei_percentage_matches_source_javascript_rounding(self):
        result = calculate_numerology("ABBBBBBB", "1988-01-15")
        self.assertEqual(result["planes"]["mental"]["count"], 1)
        self.assertEqual(result["planes"]["mental"]["ratio"], 0.125)
        self.assertEqual(result["planes"]["mental"]["percent"], 0.13)

    def test_civil_date_has_no_timezone_shift(self):
        result = calculate_numerology("Avery Morgan", "1988-01-15")
        self.assertEqual(result["birth_date_basis"], "1988-01-15")


class ApiChecks(unittest.TestCase):
    def test_health_checks_actual_astronomical_files(self):
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ready")
        self.assertFalse(response.json()["personal_report_approved"])

    def test_location_lookup_returns_coordinates_and_iana_zone(self):
        response = client.get("/api/locations", params={"q": "Los Alamitos California"})
        self.assertEqual(response.status_code, 200)
        rows = response.json()
        self.assertTrue(rows)
        self.assertEqual(rows[0]["timezone"], "America/Los_Angeles")
        self.assertIn("centroid", rows[0]["provenance"])

    def test_manual_coordinate_timezone_uses_local_polygon_data(self):
        response = client.get("/api/timezone", params={"latitude": 33.8044, "longitude": -118.0673})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["timezone"], "America/Los_Angeles")

    def test_invalid_form_does_not_echo_personal_data(self):
        response = client.post("/api/compare", json=generic_input(birth_date="1988-02-31"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "INVALID_FORM")
        self.assertNotIn("Avery", response.text)
        self.assertNotIn("input", response.json()["error"])

    def test_missing_time_suppresses_all_houses_and_angles(self):
        response = client.post("/api/compare", json=generic_input(
            birth_time=None, time_accuracy="unknown"))
        self.assertEqual(response.status_code, 200, response.text[:1000])
        result = response.json()
        self.assertTrue(result["chart"]["time"]["time_is_reference_only"])
        self.assertEqual(result["chart"]["angles"], {})
        for row in result["chart"]["points"]:
            if row.get("available"):
                self.assertIsNone(row.get("house"))
                self.assertIsNone(row.get("field"))
        self.assertFalse(result["stored_server_side"])
        self.assertFalse(result["personal_report_approved"])

    def test_dst_gap_requires_correction(self):
        response = client.post("/api/compare", json=generic_input(
            birth_date="2024-03-10", birth_time="02:30"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "NONEXISTENT_DST_TIME")

    def test_dst_overlap_requires_occurrence_choice(self):
        response = client.post("/api/compare", json=generic_input(
            birth_date="2024-11-03", birth_time="01:30"))
        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json()["error"]["code"], "AMBIGUOUS_DST_FOLD")
        self.assertEqual(len(response.json()["error"]["details"]["choices"]), 2)

    def test_bad_time_and_nonfinite_coordinates_are_rejected(self):
        self.assertEqual(client.post("/api/compare", json=generic_input(
            birth_time="25:01")).status_code, 422)
        self.assertEqual(client.post("/api/compare", json=generic_input(
            latitude=91)).status_code, 422)

    def test_cross_origin_post_is_not_accepted(self):
        response = client.post("/api/compare", json=generic_input(),
                               headers={"Origin": "https://unrelated.example"})
        self.assertEqual(response.status_code, 403)


if __name__ == "__main__":
    unittest.main(verbosity=2)

