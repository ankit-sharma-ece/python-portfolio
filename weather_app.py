import urllib.request
import urllib.parse
import urllib.error
import json
import datetime
import time
import os

RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
RED    = "\033[91m"
BLUE   = "\033[94m"
WHITE  = "\033[97m"
GRAY   = "\033[90m"

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def get_weather_emoji(code):
    if code == 113: return "☀️ "
    elif code == 116: return "⛅"
    elif code == 119: return "☁️ "
    elif code in [143,248,260]: return "🌫️ "
    elif code in [176,263,266,281,284]: return "🌦️ "
    elif code in [179,323,326,329,332,335,338]: return "🌨️ "
    elif code in [182,185,311,314,317,350]: return "🌧️ "
    elif code in [200,386,389,392,395]: return "⛈️ "
    elif code in [227,230]: return "❄️ "
    elif code in [293,296,299,302,305,308]: return "🌧️ "
    else: return "🌡️ "

def loading_animation(msg="Fetching weather"):
    frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    for i in range(20):
        print(f"\r  {CYAN}{frames[i%10]}{RESET} {msg}...", end="", flush=True)
        time.sleep(0.08)
    print("\r" + " "*40 + "\r", end="")

def fetch_weather(city):
    city_encoded = urllib.parse.quote(city)
    url = f"https://wttr.in/{city_encoded}?format=j1"
    req = urllib.request.Request(url, headers={"User-Agent": "WeatherApp/1.0"})
    try:
        response = urllib.request.urlopen(req, timeout=10)
        data = json.loads(response.read().decode("utf-8"))
        if "current_condition" not in data or "weather" not in data:
            return None
        return data
    except Exception:
        return None

def get_city_name(data, fallback="Unknown"):
    try:
        return data["nearest_area"][0]["areaName"][0]["value"]
    except Exception:
        return fallback

def get_country_name(data):
    try:
        return data["nearest_area"][0]["country"][0]["value"]
    except Exception:
        return ""

def get_region_name(data):
    try:
        return data["nearest_area"][0]["region"][0]["value"]
    except Exception:
        return ""

def display_current(data, city):
    curr      = data["current_condition"][0]
    area_name = get_city_name(data, city)
    country   = get_country_name(data)
    region    = get_region_name(data)
    temp_c    = curr.get("temp_C","N/A")
    feels     = curr.get("FeelsLikeC","N/A")
    humidity  = curr.get("humidity","N/A")
    wind_kmph = curr.get("windspeedKmph","N/A")
    wind_dir  = curr.get("winddir16Point","N/A")
    visibility= curr.get("visibility","N/A")
    pressure  = curr.get("pressure","N/A")
    uv        = curr.get("uvIndex","N/A")
    desc      = curr["weatherDesc"][0]["value"] if curr.get("weatherDesc") else "N/A"
    code      = int(curr.get("weatherCode",113))
    emoji     = get_weather_emoji(code)
    now       = datetime.datetime.now().strftime("%d %b %Y, %I:%M %p")

    print(BOLD + CYAN)
    print("  ╔══════════════════════════════════════════════════╗")
    print(("  ║   🌍  " + area_name + ", " + region)[:55].ljust(55) + "║")
    print(("  ║   📍  " + country + "  •  " + now)[:55].ljust(55) + "║")
    print("  ╚══════════════════════════════════════════════════╝" + RESET)
    print()
    print(f"  {emoji}  {BOLD}{WHITE}{temp_c}°C{RESET}  {GRAY}(Feels like {feels}°C){RESET}")
    print(f"  {YELLOW}📋 {desc}{RESET}")
    print()
    stats = [
        ("💧 Humidity",   f"{humidity}%"),
        ("💨 Wind",       f"{wind_kmph} km/h {wind_dir}"),
        ("👁️  Visibility", f"{visibility} km"),
        ("🌡️  Pressure",  f"{pressure} hPa"),
        ("☀️  UV Index",   f"{uv}"),
    ]
    print(f"  {BOLD}{'─'*42}{RESET}")
    for label, val in stats:
        print(f"  {CYAN}{label:<18}{RESET} {WHITE}{val}{RESET}")
    print(f"  {BOLD}{'─'*42}{RESET}")

def display_forecast(data):
    print(f"\n  {BOLD}{YELLOW}📅 3-DAY FORECAST:{RESET}\n")
    days = ["Today","Tomorrow","Day After"]
    for i, weather in enumerate(data["weather"][:3]):
        date    = weather.get("date","")
        max_c   = weather.get("maxtempC","N/A")
        min_c   = weather.get("mintempC","N/A")
        hourly  = weather.get("hourly",[])
        h       = hourly[4] if len(hourly) > 4 else {}
        desc    = h["weatherDesc"][0]["value"] if h.get("weatherDesc") else "N/A"
        code    = int(h.get("weatherCode",113))
        emoji   = get_weather_emoji(code)
        rain    = h.get("chanceofrain","0")
        sunrise = weather.get("astronomy",[{}])[0].get("sunrise","N/A")
        sunset  = weather.get("astronomy",[{}])[0].get("sunset","N/A")
        print(f"  {BOLD}{days[i]} ({date}){RESET}")
        print(f"  {emoji} {desc}")
        print(f"  🔺 {RED}{max_c}°C{RESET}  🔻 {BLUE}{min_c}°C{RESET}  🌧️  Rain: {rain}%")
        print(f"  🌅 Sunrise: {sunrise}  🌇 Sunset: {sunset}")
        if i < 2:
            print(f"  {GRAY}{'·'*40}{RESET}")
    print()

def display_hourly(data):
    print(f"\n  {BOLD}{YELLOW}⏰ TODAY'S HOURLY FORECAST:{RESET}\n")
    today = data["weather"][0].get("hourly",[])
    hour_labels = ["12 AM","3 AM","6 AM","9 AM","12 PM","3 PM","6 PM","9 PM"]
    print(f"  {CYAN}{'Time':<8}{'Temp':>6}{'Rain%':>8}{'Wind':>10}  Condition{RESET}")
    print(f"  {'─'*52}")
    for i, hour in enumerate(today):
        label = hour_labels[i] if i < len(hour_labels) else ""
        temp  = hour.get("tempC","N/A")
        rain  = hour.get("chanceofrain","0")
        wind  = hour.get("windspeedKmph","N/A")
        desc  = hour["weatherDesc"][0]["value"][:25] if hour.get("weatherDesc") else "N/A"
        emoji = get_weather_emoji(int(hour.get("weatherCode",113)))
        print(f"  {WHITE}{label:<8}{temp:>5}°C{rain:>7}%{wind:>8}km/h  {emoji} {desc}{RESET}")
    print()

def compare_cities():
    print(f"\n  {BOLD}{CYAN}🆚 CITY COMPARISON{RESET}\n")
    city1 = input("  Enter first city: ").strip()
    city2 = input("  Enter second city: ").strip()
    if not city1 or not city2:
        print(f"  {RED}❌ Please enter both city names!{RESET}")
        return
    loading_animation(f"Comparing {city1} & {city2}")
    d1 = fetch_weather(city1)
    d2 = fetch_weather(city2)
    if not d1:
        print(f"  {RED}❌ '{city1}' not found! Please check spelling.{RESET}")
        return
    if not d2:
        print(f"  {RED}❌ '{city2}' not found! Please check spelling.{RESET}")
        return
    c1 = d1["current_condition"][0]
    c2 = d2["current_condition"][0]
    n1 = get_city_name(d1, city1)
    n2 = get_city_name(d2, city2)
    print(f"\n  {BOLD}{'':>4} {n1:<20} {n2:<20}{RESET}")
    print(f"  {'─'*44}")
    fields = [
        ("🌡️  Temp",      c1.get("temp_C","N/A")+"°C",          c2.get("temp_C","N/A")+"°C"),
        ("💧 Humidity",   c1.get("humidity","N/A")+"%",          c2.get("humidity","N/A")+"%"),
        ("💨 Wind",       c1.get("windspeedKmph","N/A")+" km/h", c2.get("windspeedKmph","N/A")+" km/h"),
        ("👁️  Visibility", c1.get("visibility","N/A")+" km",     c2.get("visibility","N/A")+" km"),
    ]
    for label, v1, v2 in fields:
        print(f"  {CYAN}{label:<14}{RESET} {WHITE}{v1:<20}{v2:<20}{RESET}")
    try:
        t1 = int(c1.get("temp_C",0))
        t2 = int(c2.get("temp_C",0))
        if t1 > t2:
            print(f"\n  🔥 {n1} is hotter! (+{t1-t2}°C)")
        elif t2 > t1:
            print(f"\n  🔥 {n2} is hotter! (+{t2-t1}°C)")
        else:
            print(f"\n  ⚖️  Both cities have the same temperature!")
    except Exception:
        pass

def main():
    clear()
    print(BOLD + CYAN)
    slow_print("  ╔══════════════════════════════════════╗")
    slow_print("  ║   🌦️   WEATHER APP  🌦️              ║")
    slow_print("  ║      by Ankit Sharma, Rohtak         ║")
    slow_print("  ╚══════════════════════════════════════╝" + RESET)
    time.sleep(0.2)
    while True:
        print(f"\n  {BOLD}MENU:{RESET}")
        print("  1. 🌡️  Current Weather")
        print("  2. 📅  3-Day Forecast")
        print("  3. ⏰  Hourly Forecast (today)")
        print("  4. 🆚  2 Cities Comparison")
        print("  0. 🚪  Exit")
        choice = input(f"\n  {CYAN}Choose option: {RESET}").strip()
        if choice in ["1","2","3"]:
            city = input("  Enter city name (e.g. Rohtak, Delhi, Mumbai): ").strip()
            if not city:
                continue
            loading_animation(city)
            data = fetch_weather(city)
            if not data:
                print(f"  {RED}❌ City not found or no internet!{RESET}")
                input(f"\n  {GRAY}Press Enter to continue...{RESET}")
                clear()
                continue
            clear()
            if choice == "1":
                display_current(data, city)
            elif choice == "2":
                display_current(data, city)
                display_forecast(data)
            elif choice == "3":
                display_current(data, city)
                display_hourly(data)
        elif choice == "4":
            compare_cities()
        elif choice == "0":
            print(BOLD + GREEN + "\n  Goodbye! Stay safe! 🌈👋\n" + RESET)
            break
        else:
            print(f"  {RED}❌ Galat option!{RESET}")
        input(f"\n  {GRAY}Press Enter to go back to menu...{RESET}")
        clear()

if __name__ == "__main__":
    main()
