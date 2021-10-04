from django.db import models

# Create your models here.

class Record(models.Model):
    """
    Record model
    """

    status_choices = models.IntegerChoices("Status_Choices","Pending Processing Completed Error NotFound")

    status = models.IntegerField(choices=status_choices.choices,default=status_choices.Pending)
    meeting_id = models.CharField(max_length=64,primary_key=True)
    video = models.FilePathField(blank=True)
    task_id = models.CharField(max_length=64,blank=True)
    def is_processed(self):
        """check if record is already processed
        :returns: True if processed and False if not

        """

        if self.status == self.status_choices.Completed:
            return True

        return False
