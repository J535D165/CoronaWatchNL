## :chart_with_upwards_trend: Forecast charts

The following graphs show the development of Coronavirus on a daily basis. The underlying data can be found in the [data folder](/data). The [graphs](/plots) are updated on an hourly basis and were generated automatically. Please validate the numbers in the graphs before publishing. See the license section for information about sharing the graphs.

The first predictions are based on exponential growth model.
![plots/prediction.png](plots/prediction.png)

Note, however that the data no longer behave exponentially. If we plot them on
a log axis they deviate from the line quite drastically!
![plots/prediction_log10.png](plots/prediction_log10.png)

Thus we try to fit a sigmoidal curve. One way to fit this, is to first estimate
the growth rate, which we define here as the ratio of new cases over previous
new cases. Once this growth rate reaches 1, it is likely that the data will
stop following an exponential pattern and will taper down into a sigmoid
curvature.

Here is the development of the growth factor over time, with a linear model fit
to try to estimate when the inflection point will occur (or has occurred).

![plots/growthfactor.png](plots/growthfactor.png)

This then results in the following sigmoidal fit:
![plots/sigmoid.png](plots/sigmoid.png)

For more information about this approach, please watch
[the YouTube video](https://www.youtube.com/watch?v=Kas0tIxDvrg) that inspired
this approach, by Grant Sanderson
([3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)).
