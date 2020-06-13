from django.db import models as m


class Weather(m.Model):
    data=m.DateTimeField(null=True, blank=True)
    we = m.IntegerField(null=True, blank=True)
    city=m.TextField(null=True, blank=True)

    def same_data(self):
        for p in Weather.objects.all():
            #print(p.data.strftime("%d-%m-%Y %H"), self.data.strftime("%d-%m-%Y %H"))
            if p.data.strftime("%d-%m-%Y %H")==self.data.strftime("%d-%m-%Y %H"):
                if p.city==self.city:
                    return  False
        return True

    class Meta:
        verbose_name_plural = "Weather"

    def __str__(self):
        return f"Weather(id={self.pk},C={self.we!r})"



