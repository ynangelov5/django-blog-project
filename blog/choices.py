from django.db import models

class ReactionType(models.TextChoices):
    LIKE = 'LIKE', 'Like'
    DISLIKE = 'DISLIKE', 'Dislike'


class ReportReason(models.TextChoices):
    SPAM = 'SPAM', 'Spam'
    ADVERTISEMENT = 'ADVERTISEMENT', 'Advertisement'
    BULLYING = 'BULLYING', 'Bullying'
    INAPPROPRIATE = 'INAPPROPRIATE', 'Inappropriate Content'
    OTHER = 'OTHER', 'Other'
