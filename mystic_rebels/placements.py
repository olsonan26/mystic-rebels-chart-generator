from math import floor,isfinite
SIGNS=('Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces')
RULERS=('Mars','Venus','Mercury','Moon','Sun','Mercury','Venus','Pluto','Jupiter','Saturn','Uranus','Neptune')

def norm(value):
    if not isfinite(value):raise ValueError('Non-finite angle')
    return value%360

def house(longitude,ascendant):return (floor(norm(longitude)/30)-floor(norm(ascendant)/30))%12+1

def derive(longitude,ascendant=None):
    raw=norm(longitude);sign=floor(raw/30);within=raw%30;decan=floor(within/10)
    # Same-element decans advance by four signs from the astronomical sign.
    h=house(raw,ascendant) if ascendant is not None else None
    return {'sign':SIGNS[sign],'sign_index':sign,'degree_in_sign':within,'degree_floor':floor(within),'decan':decan+1,'tone':SIGNS[sign],'pulse':SIGNS[(sign+4*decan)%12],'house':h,'field':SIGNS[h-1] if h else None,'true_placement':SIGNS[h-1] if h else None,'sign_ruler':RULERS[sign],'spark':None}

def dms(longitude):
    # Round only for display, carrying across sign boundaries without modifying raw data.
    total=round(norm(longitude)*3600)%1296000
    return f'{SIGNS[total//108000]} {(total%108000)//3600}°{(total%3600)//60:02d}′{total%60:02d}″'
