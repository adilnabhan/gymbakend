from django.db import models


class Gym(models.Model):
    """Fitness center / gym listing across India."""

    # ── Basic Info ────────────────────────────────────────────────────────
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    secondary_phone = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)

    # ── Categories & Amenities ────────────────────────────────────────────
    categories = models.JSONField(default=list, blank=True, help_text='e.g. ["Gym","Fitness","Crossfit"]')
    amenities = models.JSONField(default=list, blank=True, help_text='e.g. ["Parking","CCTV","WiFi"]')

    # ── Location ──────────────────────────────────────────────────────────
    city = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100, db_index=True)
    building_name = models.CharField(max_length=200, blank=True)
    street = models.CharField(max_length=200, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)

    # ── Social Media ──────────────────────────────────────────────────────
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    youtube = models.URLField(blank=True)

    # ── Schedule: Monday ──────────────────────────────────────────────────
    monday_open = models.BooleanField(default=True)
    monday_morning_open = models.TimeField(default='06:00')
    monday_morning_close = models.TimeField(default='10:00')
    monday_evening_open = models.TimeField(default='17:00')
    monday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Tuesday ─────────────────────────────────────────────────
    tuesday_open = models.BooleanField(default=True)
    tuesday_morning_open = models.TimeField(default='06:00')
    tuesday_morning_close = models.TimeField(default='10:00')
    tuesday_evening_open = models.TimeField(default='17:00')
    tuesday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Wednesday ───────────────────────────────────────────────
    wednesday_open = models.BooleanField(default=True)
    wednesday_morning_open = models.TimeField(default='06:00')
    wednesday_morning_close = models.TimeField(default='10:00')
    wednesday_evening_open = models.TimeField(default='17:00')
    wednesday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Thursday ────────────────────────────────────────────────
    thursday_open = models.BooleanField(default=True)
    thursday_morning_open = models.TimeField(default='06:00')
    thursday_morning_close = models.TimeField(default='10:00')
    thursday_evening_open = models.TimeField(default='17:00')
    thursday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Friday ──────────────────────────────────────────────────
    friday_open = models.BooleanField(default=True)
    friday_morning_open = models.TimeField(default='06:00')
    friday_morning_close = models.TimeField(default='10:00')
    friday_evening_open = models.TimeField(default='17:00')
    friday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Saturday ────────────────────────────────────────────────
    saturday_open = models.BooleanField(default=True)
    saturday_morning_open = models.TimeField(default='06:00')
    saturday_morning_close = models.TimeField(default='10:00')
    saturday_evening_open = models.TimeField(default='17:00')
    saturday_evening_close = models.TimeField(default='21:00')

    # ── Schedule: Sunday ──────────────────────────────────────────────────
    sunday_open = models.BooleanField(default=False)

    # ── Meta ──────────────────────────────────────────────────────────────
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'name']
        verbose_name_plural = 'gyms'

    def __str__(self):
        return f"{self.name} – {self.city}"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(f"{self.name}-{self.city}")
        super().save(*args, **kwargs)
