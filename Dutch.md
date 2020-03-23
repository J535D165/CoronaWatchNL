

# Ontwikkeling van het coronavirus, gebaseerd op RIVM data


Op 31 december 2019 werd in Wuhan, China de eerste besmetting met het Coronavirus (COVID-19) gemeld. Op 27 februari 2020 werd het eerste geval in Nederland gemeld door de RIVM. Binnen een week werden meer dan honderd nieuwe gevallen bevestigd. Het RIVM vermeldt de aantallen positief geteste mensen op hun [website](https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus).

Vanaf 3 maart vermeldt het RIVM ook dagelijks de aantallen per gemeente op de website. De dataset bevat niet alle besmette personen, alleen de positief geteste gevallen. Verder vermeldt het RIVM op dit moment ook geen beter gemelde personen. ~De  [ruwe data]( https://www.volksgezondheidenzorg.info/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19#definities) is te vinden op deze site van de overheid https://www.volksgezondheidenzorg.info.~ De meest recente aantallen kunnen gevonden worden op https://www.rivm.nl/coronavirus-kaart-van-nederland. 

## Dit project :exclamation: Dagelijkse updates :exclamation:

Op dit moment delen RIVM en https://www.volksgezondheidenzorg.info geen datasets met de datum van diagnose op de sites. Het is daarom lastig om een overzicht te krijgen van het tijdsverloop (en gemeente). Deze informatie is belangrijk voor journalisten, onderzoekers en iedereen die geinteresseerd is. Dit project downloadt daarom **ieder uur** de laatste gegevens van de RIVM naar de repo. In de map [raw_data/](raw_data/) is deze gedownloade en niet-verwerkte data van het RIVM te vinden. De map [data/](data/) bevat datasets die gereed gemaakt zijn voor analyse. 

Datasets:

  - :page_facing_up: [RIVM Coronavirus: Positief geteste patienten in Nederland](data/rivm_corona_in_nl_daily.csv) 
  - :page_facing_up: [RIVM Coronavirus: overleden patienten in Nederland](data/rivm_corona_in_nl_fatalities.csv) 
  - :page_facing_up: [RIVM Coronavirus: opgenomen patienten in Nederland](data/rivm_corona_in_nl_hosp.csv) 
  - :page_facing_up: RIVM Coronavirus: aantallen per gemeente  in Nederland [[long format]](data/rivm_corona_in_nl.csv) [[wide format]](data/rivm_corona_in_nl_table.csv) 

For academisch gebruik is er deze vermelding:  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575) en hier zijn de voorwaarden te vinden [License and academic use](#license-and-academic-use)



## Help ons

Hulp wordt gewaardeerd! We zijn op zoek naar nieuwe grafieken, kaarten, verrijkte datasets en interactieve visualisaties. 

Vermeld problemen svp in de [Issue Tracker](https://github.com/J535D165/CoronaWatchNL/issues) van Github. 

Wil je helpen? Kijk dan naar de issues met een `help wanted` vermelding in de [Issue Tracker](https://github.com/J535D165/CoronaWatchNL/issues).

Lees https://github.com/J535D165/CoronaWatchNL/actions and [/.github/workflows](/.github/workflows) voor technische details rond data verzameling en het ophalen ervan op geplande tijdstippen.

## :chart_with_upwards_trend: Grafieken

De volgende grafieken laten de dagelijkse ontwikkeling van het Coronavirus zien. De bijhorende data is hier te vinden: [data/rivm_corona_in_nl.csv](data/rivm_corona_in_nl.csv). De [grafieken](/graphs) worden ieder uur bijgewerkt en worden automatisch gegenereerd. Controleer de getallen voor publicatie en lees het deel over licenties voor deze te delen. 

![plots/timeline.png](plots/timeline.png)

![plots/top_municipalities.png](plots/top_municipalities.png)

![plots/timeline.png](plots/province_count.png)

![plots/province_count_time.png](plots/province_count_time.png)


### Kaarten

![plots/map_province.png](plots/map_province.png)

![plots/map_nl_corona_abs_municipality.gif?raw=true](plots/map_nl_corona_abs_municipality.gif?raw=true)
![plots/map_nl_corona_diff_municipality.gif?raw=true](plots/map_nl_corona_diff_municipality.gif?raw=true)

### Voorspellingen

De eerste voorspellingen zijn gebaseerd op modellen voor exponentiele groei. ![plots/prediction.png](plots/prediction.png)

De data laat nu echter een ander beeld zien dan exponentiele groei. Als we de data op een logaritmische schaal zetten, dan wijkt de data drastisch af van de lijn!
![plots/prediction_log10.png](plots/prediction_log10.png)

We proberen daarom een sigmoide functie. Een manier om dit passend te maken, is om de mate van groei te bepalen. Deze definieren we als de ratio van nieuwe gevallen over nieuwe gevallen uit de eerdere periode. Asl deze ratio 1 bereikt, dan is de kans groot dat de groei geen exponentiele curve volgt, maar afneemt naar een sigmoide functie. Hier is de ontwikkeling van de groeifactor over tijd, met een lineair model om te bepalen wanneer dit moment zich voor zal doen. 

![plots/growthfactor.png](plots/growthfactor.png)

Dit leidt dan tot de volgende sigmoide functie:
![plots/sigmoid.png](plots/sigmoid.png)

Voor meer informatie over de aanpak, is er deze [YouTube video](https://www.youtube.com/watch?v=Kas0tIxDvrg) door Grant Sanderson, die ons inspireerde tot deze aanpak
([3Blue1Brown](https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw)).

## Interessante links

- https://medium.com/@tomaspueyo/coronavirus-act-today-or-people-will-die-f4d3d9cd99ca
- http://www.casperalbers.nl/nl/post/2020-03-11-coronagrafieken/
- https://worktimesheet2014.blogspot.com/2020/03/coronovirus-in-netherlands-power-bi.html (Made with CoronaWatchNL data)
- https://www.youtube.com/watch?v=Kas0tIxDvrg

## Licentie and academisch gebruik

De grafieken en data vallen on de de volgende licentie [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/). De originele data is copyright RIVM. 

Voor academic gebruik, gebruik presistente data van [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575). Dit is een kopie van de data die ongewijzigd blijft. Het versienummer verwijst naar de datum. Please cite:

```De Bruin, J. (2020). Number of diagnoses with coronavirus disease (COVID-19) in The Netherlands (Version v2020.3.15) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.3711575```

Image from [iXimus](https://pixabay.com/nl/users/iXimus-2352783/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881) via [Pixabay](https://pixabay.com/nl/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881)

## Contact

Stuur een mail naar jonathandebruinos@gmail.com

