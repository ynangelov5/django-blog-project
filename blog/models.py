from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.urls import reverse
from blog.choices import ReactionType, ReportReason
from utils.mixins import Timestamps 

"""
TODO unique_together may be deprecated,
use UniqueConstraint (also in the meta class)
Low priority
"""

class Post(Timestamps):
    title = models.CharField(
        max_length=100, 
        validators=[MinLengthValidator(2)]
    )
    content = models.TextField(
        max_length=10_000,
        validators=[MinLengthValidator(10)]
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
#TODO consider making an abstract/base reaction model
class PostReaction(Timestamps):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="post_reactions"
    )
    post = models.ForeignKey(
        to='Post',
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    reaction = models.CharField(
        max_length=20,
        choices=ReactionType.choices
    )

    class Meta:
        unique_together = ('user', 'post')
        indexes = [
            models.Index(fields=['post', 'reaction']),
        ]

    def __str__(self):
        return f"{self.user.username} reacted with '{self.get_reaction_display()}' " \
               f"to post {self.post.title}"
    

class Comment(Timestamps):
    post = models.ForeignKey(
        to='Post',
        on_delete=models.CASCADE,
        related_name="comments"
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    content = models.CharField(
        max_length=1000,
        validators=[MinLengthValidator(1)]
    )
    # created != updated_at can check if a comment has been edited

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


class CommentReaction(Timestamps):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="comment_reactions"
    )
    comment = models.ForeignKey(
        to='Comment',
        on_delete=models.CASCADE,
        related_name="reactions"
    )
    reaction = models.CharField(
        max_length=20,
        choices=ReactionType.choices
    )

    class Meta:
        unique_together = ('user', 'comment')
        indexes = [
            models.Index(fields=['comment', 'reaction']),
        ]

    def __str__(self):
        return f"{self.user.username} reacted with '{self.get_reaction_display()}' " \
               f"to {self.comment.user.username}'s comment"
    

class BaseReport(Timestamps):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="%(class)s_reports"
    )
    reason = models.CharField(
        max_length=30,
        choices=ReportReason.choices
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    is_resolved = models.BooleanField(
        default=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.user.username} reported {self.target} for {self.reason}"


class PostReport(BaseReport):
    post = models.ForeignKey(
        to='Post',
        on_delete=models.CASCADE,
        related_name="reports"
    )

    class Meta:
        unique_together = ('user', 'post')

    @property
    def target(self):
        return self.post


class CommentReport(BaseReport):
    comment = models.ForeignKey(
        to='Comment',
        on_delete=models.CASCADE,
        related_name="reports"
    )

    class Meta:
        unique_together = ('user', 'comment')

    @property
    def target(self):
        return self.comment


class UserReport(BaseReport):
    reported_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="reported_by"
    )

    class Meta:
        unique_together = ('user', 'reported_user')

    @property
    def target(self):
        return self.reported_user


class Follow(Timestamps):
    follower = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="followed_people"
    )
    followed = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="followers"
    )

    class Meta:
        unique_together = ('follower', 'followed')




