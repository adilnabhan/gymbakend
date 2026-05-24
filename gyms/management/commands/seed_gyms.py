"""
Seed ~500 gyms across India with realistic data.
Usage: python manage.py seed_gyms
       python manage.py seed_gyms --clear
"""
import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from gyms.models import Gym


# ── 50 cities with (city, state, lat, lng, pin_prefix) ───────────────────
CITIES = [
    ("Kozhikode", "Kerala", 11.2588, 75.7804, "673"),
    ("Kochi", "Kerala", 9.9312, 76.2673, "682"),
    ("Thiruvananthapuram", "Kerala", 8.5241, 76.9366, "695"),
    ("Thrissur", "Kerala", 10.5276, 76.2144, "680"),
    ("Kannur", "Kerala", 11.8745, 75.3704, "670"),
    ("Malappuram", "Kerala", 11.0510, 76.0711, "676"),
    ("Kollam", "Kerala", 8.8932, 76.6141, "691"),
    ("Mumbai", "Maharashtra", 19.0760, 72.8777, "400"),
    ("Pune", "Maharashtra", 18.5204, 73.8567, "411"),
    ("Nagpur", "Maharashtra", 21.1458, 79.0882, "440"),
    ("Nashik", "Maharashtra", 19.9975, 73.7898, "422"),
    ("Thane", "Maharashtra", 19.2183, 72.9781, "400"),
    ("Delhi", "Delhi", 28.7041, 77.1025, "110"),
    ("Noida", "Uttar Pradesh", 28.5355, 77.3910, "201"),
    ("Gurgaon", "Haryana", 28.4595, 77.0266, "122"),
    ("Bangalore", "Karnataka", 12.9716, 77.5946, "560"),
    ("Mysuru", "Karnataka", 12.2958, 76.6394, "570"),
    ("Mangalore", "Karnataka", 12.9141, 74.8560, "575"),
    ("Hyderabad", "Telangana", 17.3850, 78.4867, "500"),
    ("Chennai", "Tamil Nadu", 13.0827, 80.2707, "600"),
    ("Coimbatore", "Tamil Nadu", 11.0168, 76.9558, "641"),
    ("Madurai", "Tamil Nadu", 9.9252, 78.1198, "625"),
    ("Kolkata", "West Bengal", 22.5726, 88.3639, "700"),
    ("Ahmedabad", "Gujarat", 23.0225, 72.5714, "380"),
    ("Surat", "Gujarat", 21.1702, 72.8311, "395"),
    ("Vadodara", "Gujarat", 22.3072, 73.1812, "390"),
    ("Jaipur", "Rajasthan", 26.9124, 75.7873, "302"),
    ("Udaipur", "Rajasthan", 24.5854, 73.7125, "313"),
    ("Jodhpur", "Rajasthan", 26.2389, 73.0243, "342"),
    ("Lucknow", "Uttar Pradesh", 26.8467, 80.9462, "226"),
    ("Varanasi", "Uttar Pradesh", 25.3176, 82.9739, "221"),
    ("Agra", "Uttar Pradesh", 27.1767, 78.0081, "282"),
    ("Chandigarh", "Chandigarh", 30.7333, 76.7794, "160"),
    ("Amritsar", "Punjab", 31.6340, 74.8723, "143"),
    ("Ludhiana", "Punjab", 30.9010, 75.8573, "141"),
    ("Indore", "Madhya Pradesh", 22.7196, 75.8577, "452"),
    ("Bhopal", "Madhya Pradesh", 23.2599, 77.4126, "462"),
    ("Patna", "Bihar", 25.6093, 85.1376, "800"),
    ("Bhubaneswar", "Odisha", 20.2961, 85.8245, "751"),
    ("Guwahati", "Assam", 26.1445, 91.7362, "781"),
    ("Dehradun", "Uttarakhand", 30.3165, 78.0322, "248"),
    ("Ranchi", "Jharkhand", 23.3441, 85.3096, "834"),
    ("Raipur", "Chhattisgarh", 21.2514, 81.6296, "492"),
    ("Goa", "Goa", 15.2993, 74.1240, "403"),
    ("Visakhapatnam", "Andhra Pradesh", 17.6868, 83.2185, "530"),
    ("Vijayawada", "Andhra Pradesh", 16.5062, 80.6480, "520"),
    ("Hubli", "Karnataka", 15.3647, 75.1240, "580"),
    ("Faridabad", "Haryana", 28.4089, 77.3178, "121"),
    ("Navi Mumbai", "Maharashtra", 19.0330, 73.0297, "410"),
    ("Kolhapur", "Maharashtra", 16.7050, 74.2433, "416"),
]

# ── Gym names (realistic Indian gym brands) ──────────────────────────────
GYM_NAMES = [
    "The Belly Gym", "FITZO Fitness Center", "Klaan Fitness", "Iron Temple",
    "Muscle Garage", "FitLife Studio", "PowerZone Gym", "Alpha Fitness Hub",
    "CrossFit Arena", "Body Sculptor Gym", "Shred Factory", "Endurance Fitness",
    "Spartan Gym", "Titan Fitness Club", "Pump House Gym", "Core Strength Studio",
    "Viking Fitness", "Beast Mode Gym", "Elite Gym", "The Grind House",
    "Sweat Zone Gym", "Flex Fitness", "Ignite Gym", "Urban Fitness Studio",
    "Peak Performance Gym", "Warrior Fitness", "Gravity Gym", "Forge Fitness",
    "Apex Gym", "Zen Fitness Studio", "Metro Gym", "Royal Fitness Club",
    "Champion Gym", "Dynamo Fitness", "Blaze Gym", "Storm Fitness",
    "Hustle Gym", "Edge Fitness Center", "Summit Gym", "Platinum Fitness",
    "Diamond Gym", "Legend Fitness Club", "Thunder Gym", "Evolve Fitness",
    "Transform Studio", "Phoenix Gym", "Bolt Fitness", "Rage Gym",
    "Muscle Mantra", "FitFreak Gym", "Power Play Gym", "Adrenaline Fitness",
    "Fit India Gym", "Desi Gains Gym", "Swasthya Gym", "Shakti Fitness",
    "Aarogyam Gym", "Surya Fitness", "Vajra Gym", "Prana Fitness Studio",
    "Kalari Gym", "Malabar Fitness", "Sahyadri Gym", "Nila Fitness",
    "Rocky's Gym", "Arnold's Gym", "The Fitness Factory", "G-Force Gym",
    "Max Fitness Studio", "ProFit Gym", "Total Fitness", "Absolute Gym",
    "Xtreme Fitness", "NexGen Gym", "FitHub", "GymWorks",
    "The Iron Lab", "Steel Gym", "Muscle Kitchen", "BodyCraft Gym",
]

# ── Streets / localities ─────────────────────────────────────────────────
STREETS = [
    "East Nadakkave", "Mavoor Road", "Palazhi Road", "Kallai Road",
    "MG Road", "Brigade Road", "Church Street", "Commercial Street",
    "Jubilee Hills Road", "Banjara Hills", "Hitech City Main Road",
    "Anna Salai", "Mount Road", "T Nagar Main Road", "ECR Road",
    "Park Street", "Salt Lake Sector V", "New Town Main Road",
    "SG Highway", "CG Road", "Ashram Road", "Satellite Road",
    "MI Road", "Tonk Road", "Malviya Nagar Road", "JLN Marg",
    "Hazratganj Road", "Gomti Nagar Main Road", "Aliganj Main Road",
    "Sector 17", "Sector 22", "Industrial Area Phase 1",
    "GT Road", "Mall Road", "Lawrence Road",
    "Linking Road", "SV Road", "Western Express Highway", "LBS Marg",
    "FC Road", "JM Road", "Karve Road", "Baner Road",
    "Station Road", "Ring Road", "Bypass Road", "National Highway",
    "Market Road", "Temple Road", "Lake Road", "Beach Road",
    "Gandhi Nagar Main Road", "Nehru Place", "Connaught Place",
    "Rajaji Road", "Palarivattom", "Edappally Bypass", "Marine Drive",
    "Vytilla Junction", "Kadavanthra Road", "MG Road Kochi",
    "Kowdiar Road", "Pattom Road", "Kesavadasapuram Road",
]

# ── Building names ───────────────────────────────────────────────────────
BUILDINGS = [
    "Fitness Tower", "Wellness Center", "Health Hub Building", "Sports Complex",
    "Power House", "Gym Plaza", "Fitness Arena", "Training Center",
    "Wellness Hub", "Performance Center", "Athletic Complex", "Muscle Mansion",
    "Fitness Point", "Gym Junction", "Body Works Building", "FitSquare",
    "Iron House", "Strength Studio", "The Gym Building", "Fitness Block",
    "Workout Center", "Cardio Tower", "Training Hub", "Sports Arena",
    "Fitness Arcade", "Gym Towers", "Athletic Center", "Health Point",
    "Power Center", "Energy Hub", "Stamina Building", "Vigor Complex",
]

# ── Categories & amenities ───────────────────────────────────────────────
CATEGORIES_POOL = [
    "Gym", "Fitness", "Crossfit", "Yoga", "Zumba", "Martial Arts",
    "Boxing", "Kickboxing", "Pilates", "Calisthenics", "Functional Training",
    "Strength Training", "Cardio", "HIIT", "Spinning", "Swimming",
    "Dance Fitness", "Aerobics", "Weight Training", "Personal Training",
]

AMENITIES_POOL = [
    "Parking", "CCTV", "WiFi", "Locker", "Steam Bath", "Sauna",
    "Swimming Pool", "Cafe", "Juice Bar", "Shower", "AC",
    "Personal Trainer", "Group Classes", "Physiotherapy", "Diet Consultation",
    "Cardio Zone", "Free Weights", "Functional Zone", "Boxing Ring",
    "Yoga Studio", "CrossFit Rig", "TRX Zone", "Battle Ropes",
    "Changing Room", "Towel Service", "Music System", "TV Screens",
]

DESCRIPTIONS = [
    "Premium fitness center with cardio and strength training",
    "Modern gym with personal training and group classes",
    "Functional and strength fitness club with expert trainers",
    "Full-service gym with state-of-the-art equipment",
    "Affordable fitness center with quality training",
    "Elite gym offering CrossFit, yoga, and weight training",
    "Community-focused gym with certified personal trainers",
    "High-performance training facility for all fitness levels",
    "Boutique fitness studio with personalized workout programs",
    "Complete fitness solution with cardio, weights, and classes",
    "Professional gym with world-class amenities and trainers",
    "Budget-friendly gym with AC, parking, and modern equipment",
    "Luxury fitness club with steam bath, sauna, and pool",
    "Neighborhood gym with friendly atmosphere and expert guidance",
    "Dedicated strength and conditioning facility",
    "Women-friendly gym with separate training zones",
    "24/7 fitness center with round-the-clock access",
    "Sports-focused gym with boxing ring and martial arts",
    "Holistic wellness center with yoga, gym, and nutrition",
    "Results-driven gym with transformation programs",
]


class Command(BaseCommand):
    help = 'Seed ~500 gyms across major Indian cities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear', action='store_true',
            help='Delete all existing gyms before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Gym.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing gyms'))

        created = 0
        # Distribute: top cities get more gyms
        tier1 = CITIES[:12]   # ~15 each = 180
        tier2 = CITIES[12:30] # ~10 each = 180
        tier3 = CITIES[30:]   # ~7 each  = 140  → total ~500

        for city_data, count in [(tier1, 15), (tier2, 10), (tier3, 7)]:
            for (city, state, lat, lng, pin_prefix) in city_data:
                used_slugs = set()
                for i in range(count):
                    gym_name = random.choice(GYM_NAMES)
                    street = random.choice(STREETS)
                    building = random.choice(BUILDINGS)

                    # Slug uniqueness
                    slug_base = slugify(f"{gym_name}-{street}-{city}")
                    slug = slug_base
                    counter = 1
                    while slug in used_slugs or Gym.objects.filter(slug=slug).exists():
                        slug = f"{slug_base}-{counter}"
                        counter += 1
                    used_slugs.add(slug)

                    # Location jitter
                    jlat = round(lat + random.uniform(-0.06, 0.06), 4)
                    jlng = round(lng + random.uniform(-0.06, 0.06), 4)

                    # Categories (2-4) and amenities (3-7)
                    cats = random.sample(CATEGORIES_POOL, random.randint(2, 4))
                    amens = random.sample(AMENITIES_POOL, random.randint(3, 7))

                    # Contact info
                    phone = f"91{random.randint(70000, 99999)}{random.randint(10000, 99999)}"
                    sec_phone = f"91{random.randint(70000, 99999)}{random.randint(10000, 99999)}"
                    name_slug = slugify(gym_name)
                    city_slug = slugify(city)
                    email = f"info@{name_slug}{city_slug}.com"

                    # Social media
                    ig = f"https://instagram.com/{name_slug}_{city_slug}"
                    fb = f"https://facebook.com/{name_slug}{city_slug}"
                    yt = f"https://youtube.com/@{name_slug}{city_slug}"
                    web = f"https://{name_slug}{city_slug}.com"

                    # Schedule variations
                    mo = random.choice(['05:00', '06:00', '06:30'])
                    mc = random.choice(['10:00', '10:30', '11:00'])
                    eo = random.choice(['16:00', '16:30', '17:00'])
                    ec = random.choice(['21:00', '21:30', '22:00'])
                    sun_open = random.choice([True, False, False])  # ~33% open Sunday

                    pincode = f"{pin_prefix}{random.randint(1, 99):03d}"

                    Gym.objects.create(
                        name=gym_name,
                        slug=slug,
                        email=email,
                        phone_number=phone,
                        secondary_phone=sec_phone,
                        description=random.choice(DESCRIPTIONS),
                        website=web,
                        categories=cats,
                        amenities=amens,
                        city=city,
                        state=state,
                        building_name=building,
                        street=street,
                        pin_code=pincode,
                        latitude=Decimal(str(jlat)),
                        longitude=Decimal(str(jlng)),
                        instagram=ig,
                        facebook=fb,
                        youtube=yt,
                        monday_open=True,
                        monday_morning_open=mo, monday_morning_close=mc,
                        monday_evening_open=eo, monday_evening_close=ec,
                        tuesday_open=True,
                        tuesday_morning_open=mo, tuesday_morning_close=mc,
                        tuesday_evening_open=eo, tuesday_evening_close=ec,
                        wednesday_open=True,
                        wednesday_morning_open=mo, wednesday_morning_close=mc,
                        wednesday_evening_open=eo, wednesday_evening_close=ec,
                        thursday_open=True,
                        thursday_morning_open=mo, thursday_morning_close=mc,
                        thursday_evening_open=eo, thursday_evening_close=ec,
                        friday_open=True,
                        friday_morning_open=mo, friday_morning_close=mc,
                        friday_evening_open=eo, friday_evening_close=ec,
                        saturday_open=True,
                        saturday_morning_open=mo, saturday_morning_close=mc,
                        saturday_evening_open=eo, saturday_evening_close=ec,
                        sunday_open=sun_open,
                        rating=Decimal(str(round(random.uniform(3.2, 4.9), 1))),
                        monthly_fee=Decimal(str(random.randint(5, 50) * 100)),
                        is_active=True,
                    )
                    created += 1

        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created} gyms across {len(CITIES)} cities'
        ))
