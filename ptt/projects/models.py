from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    # Allow infinite nesting of projects
    parent_project = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='sub_projects',
    )

    @property
    def full_name(self):
        names = [self.name]
        pp = self.parent_project
        while pp:
            names.append(pp.name)
            pp = pp.parent_project

        # reverse the list and join the names
        return ' :: '.join(reversed(names))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name_plural = 'projects'
        ordering = ['name']
