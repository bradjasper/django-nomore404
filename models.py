import re

from django.db import models

class PatternManager(models.Manager):

    def matches(self, string):
        "Check if a string matches the filters list"

        for pattern in self.values_list('regex', flat=True):
            if re.match(pattern, string):
                return True
        return False


class Pattern(models.Model):

    regex = models.CharField(max_length=255,
                             help_text="Enter a regex pattern to filter")
    description = models.TextField(null=False, blank=True)
    objects = PatternManager()

    def save(self, *args, **kwargs):

        # Delete all errors that match this pattern
        for error in ErrorRequest.objects.all():
            if re.match(self.regex, error.path):
                error.delete()

        super(Pattern, self).save(*args, **kwargs)



class ErrorRequestManager(models.Manager):

    def create_from_request(self, request):
        return ErrorRequest.objects.create(request=request,
                                           path=request.META["PATH_INFO"])


class ErrorRequest(models.Model):
    "Hold information about a 404 error request"

    path = models.TextField()
    request = models.TextField()

    objects = ErrorRequestManager()

    def save(self, *args, **kwargs):
        if not Pattern.objects.matches(self.path):
            super(ErrorRequest, self).save(*args, **kwargs)
