## :chart_with_upwards_trend: Forecast charts

The following graphs show the development of Coronavirus on a daily basis. The underlying data can be found in the [data folder](/data). The [graphs](/plots) are updated on an hourly basis and were generated automatically. Please validate the numbers in the graphs before publishing. See the license section for information about sharing the graphs.

The first predictions are based on exponential growth model.
![plots/prediction.png](/plots/prediction.png)

Note, however that the data no longer behave exponentially. If we plot them on
a log axis they deviate from the line quite drastically!
![plots/prediction_log10.png](/plots/prediction_log10.png)

Thus we try to fit a sigmoidal curve. One way to fit this, is to first estimate
the growth rate, which we define here as the ratio of new cases over previous
new cases. Once this growth rate reaches 1, it is likely that the data will
stop following an exponential pattern and will taper down into a sigmoid
curvature.

Here is the development of the growth factor over time, with a linear model fit
to try to estimate when the inflection point will occur (or has occurred).

![plots/growthfactor.png](/plots/growthfactor.png)

This then results in the following sigmoidal fit:
![plots/sigmoid.png](/plots/sigmoid.png)

As some provinces had the outbreak earlier than others, it's relevant to see the individual provinces. The same linear model is used to estimate the inflection point.
![plots/growthfactor_Drenthe.png](/plots/growthfactor_Drenthe.png)
![plots/growthfactor_Flevoland.png](/plots/growthfactor_Flevoland.png)
![plots/growthfactor_Friesland.png](/plots/growthfactor_Friesland.png)
![plots/growthfactor_Gelderland.png](/plots/growthfactor_Gelderland.png)
![plots/growthfactor_Groningen.png](/plots/growthfactor_Groningen.png)
![plots/growthfactor_Limburg.png](/plots/growthfactor_Limburg.png)
![plots/growthfactor_Noord-Brabant.png](/plots/growthfactor_Noord-Brabant.png)
![plots/growthfactor_Noord-Holland.png](/plots/growthfactor_Noord-Holland.png)
![plots/growthfactor_Overijssel.png](/plots/growthfactor_Overijssel.png)
![plots/growthfactor_Utrecht.png](/plots/growthfactor_Utrecht.png)
![plots/growthfactor_Zeeland.png](/plots/growthfactor_Zeeland.png)
![plots/growthfactor_Zuid-Holland.png](/plots/growthfactor_Zuid-Holland.png)

Also a sigmoid function per province:
![plots/sigmoid_Drenthe.png](/plots/sigmoid_Drenthe.png)
![plots/sigmoid_Flevoland.png](/plots/sigmoid_Flevoland.png)
![plots/sigmoid_Friesland.png](/plots/sigmoid_Friesland.png)
![plots/sigmoid_Gelderland.png](/plots/sigmoid_Gelderland.png)
![plots/sigmoid_Groningen.png](/plots/sigmoid_Groningen.png)
![plots/sigmoid_Limburg.png](/plots/sigmoid_Limburg.png)
![plots/sigmoid_Noord-Brabant.png](/plots/sigmoid_Noord-Brabant.png)
![plots/sigmoid_Noord-Holland.png](/plots/sigmoid_Noord-Holland.png)
![plots/sigmoid_Overijssel.png](/plots/sigmoid_Overijssel.png)
![plots/sigmoid_Utrecht.png](/plots/sigmoid_Utrecht.png)
![plots/sigmoid_Zeeland.png](/plots/sigmoid_Zeeland.png)
![plots/sigmoid_Zuid-Holland.png](/plots/sigmoid_Zuid-Holland.png)

As testing capacity is limited the numbers of positively tested people doesn't give a realistic picture of the outbreak. Using the data of people being hospitalised should give a more realistic picture.

Here is the development of the growth factor of hospitalisations over time, with a linear model fit
to try to estimate when the inflection point will occur (or has occurred).

![plots/growthfactor_hospitalisation.png](/plots/growthfactor_hospitalisation.png)

This then results in the following sigmoidal fit:
![plots/sigmoid_hospitalisation.png](/plots/sigmoid_hospitalisation.png)

Here is the development of the growth factor of fatalities over time, with a linear model fit
to try to estimate when the inflection point will occur (or has occurred).

![plots/growthfactor_fatalities.png](/plots/growthfactor_fatalities.png)

This then results in the following sigmoidal fit:
![plots/sigmoid_fatalities.png](/plots/sigmoid_fatalities.png)

For more information about this approach, please watch
[the YouTube video](https://www.youtube.com/watch?v=Kas0tIxDvrg) that inspired
this approach, by Grant Sanderson
([3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)).
