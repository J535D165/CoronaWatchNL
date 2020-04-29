library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)


pdf(NULL)
dir.create("plots")

# Set working directory to CoronaWatchNL folder
# Province data
data_prov <- read_csv("data/rivm_NL_covid19_province.csv")

# daily data
data_daily <- read_csv("data/rivm_corona_in_nl_daily.csv")
fata <- read_csv("data/rivm_corona_in_nl_fatalities.csv")
hosp <- read_csv("data/rivm_corona_in_nl_hosp.csv")

data_tests <- read_csv("data/rivm_NL_covid19_tests.csv")

measures <- read_csv("ext/maatregelen.csv") %>%
  mutate(name = forcats::fct_reorder(maatregel, start_datum))

# combine daily data
daily <- data_daily %>%
  mutate(meas = "Totaal") %>%
  bind_rows(hosp %>%
              mutate(meas = "Ziekenhuisopname")) %>%
  bind_rows(fata %>%
              mutate(meas = "Overleden"))

# combine daily increase
daily_diff <- data_daily %>%
  mutate(
    Aantal = Aantal - lag(Aantal),
    meas = "Totaal"
  ) %>%
  bind_rows(hosp %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
                meas = "Ziekenhuisopname")) %>%
  bind_rows(fata %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
                meas = "Overleden"))


daily %>%
  mutate(meas = factor(meas, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = meas)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Totaal COVID-19 patiënten") +
  ggsave("plots/overview_plot.png", width = 5.5, height=4)


daily_diff %>%
  mutate(meas = factor(meas, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = meas)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten") +
  ggsave("plots/overview_plot_diff.png", width = 5.5, height=4)


######################
### DAILY INCREASE ###
######################

# load datasets
data_national <- read_csv("data/rivm_NL_covid19_national.csv")
data_national_latest <- read_csv("data/rivm_NL_covid19_national_by_date/rivm_NL_covid19_national_by_date_latest.csv")

# mutate and combine datasets
daily_diff <- data_national %>%
  filter(Type == "Totaal") %>%
  mutate(
    Aantal = Aantal - lag(Aantal),
    meas = Type,
    Type = "Gerapporteerd",
  ) %>%
  bind_rows(data_national %>%
              filter(Type == "Ziekenhuisopname") %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
                meas = Type,
                Type = "Gerapporteerd",
              )
  ) %>%
  bind_rows(data_national %>%
              filter(Type == "Overleden") %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
                meas = Type,
                Type = "Gerapporteerd",
              )
  )

# combine daily increase (i.e., reported data) with 'latest' data (i.e., actual data)
samen <- data_national_latest %>%
  mutate(
    meas = Type,
    Type = "Werkelijk") %>%
  bind_rows(daily_diff)

# select all weekend days
weekends <- data.frame(xstart = unique(samen$Datum[as.numeric(wday(samen$Datum, label = TRUE)) == 7] - 0.2),
                       xend   = unique(samen$Datum[as.numeric(wday(samen$Datum, label = TRUE)) == 7] + 1.2))


# Plot "Toename COVID-19 patienten: Werkelijk vs. Gerapporteerd"
samen %>%
  mutate(meas = factor(meas, c("Totaal", "Ziekenhuisopname", "Overleden")),
         Type = factor(Type, c("Werkelijk", "Gerapporteerd"))
  ) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(meas, Type), colour = meas, linetype = Type)) +
  geom_line() +
  annotate("rect", xmin = weekends$xstart, xmax = weekends$xend, ymin = 0, ymax = max(samen$Aantal, na.rm = T), fill = "lightgray",
           alpha = .2) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename: Werkelijk vs. Gerapporteerd") +
  ggsave("plots/overview_plot_true_vs_reported_diff.png", width = 5.5, height=4)


#####################
#### DAILY TOTAL ####
#####################

# combine daily 'total' data (total, hospital intakes, deaths)
daily <- data_national %>%
  mutate(meas = Type,
         Type = "Gerapporteerd")


# calculate cumulative sum per measurement & combine daily total data (i.e., reported data) with 'latest' data (i.e., actual data)
samen_cum <- data_national_latest %>%
  filter(Type == "Totaal") %>%
  mutate(
    Aantal = cumsum(Aantal),
    meas = Type,
    Type = "Werkelijk",
  )%>%
  bind_rows(data_national_latest %>%
              filter(Type == "Ziekenhuisopname") %>%
              mutate(
                Aantal = cumsum(Aantal),
                meas = Type,
                Type = "Werkelijk"
              )) %>%
  bind_rows(data_national_latest %>%
              filter(Type == "Overleden") %>%
              mutate(
                Aantal = cumsum(Aantal),
                meas = Type,
                Type = "Werkelijk",
              )) %>%
  bind_rows(daily)

# Plot "Totaal COVID-19 patienten: Werkelijk vs. Gerapporteerd"
samen_cum %>%
  mutate(meas = factor(meas, c("Totaal", "Ziekenhuisopname", "Overleden")),
         Type = factor(Type, c("Werkelijk", "Gerapporteerd"))) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(meas, Type), colour = meas, linetype = Type))+
  geom_line() +
  annotate("rect", xmin = weekends$xstart, xmax = weekends$xend, ymin = 0, ymax = max(samen_cum$Aantal, na.rm = T), fill = "lightgray",
           alpha = .2) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9","#999999")) +
  ggtitle("Totaal: Werkelijk vs. Gerapporteerd") +
  ggsave("plots/overview_plot_true_vs_reported.png", width = 5.5, height=4)

##################
#### REPORTS #####
##################

# Read all files in the folder into one dataframe
read_plus <- function(flnm) {
  read_csv(flnm) %>%
    mutate(filename = flnm)
}

reports <-
  list.files("./data/rivm_NL_covid19_national_by_date", pattern = "*.csv",
             full.names =T) %>%
  map_df(~read_plus(.))

# Transform the original filename to shorter report date
reports <- reports[!(grepl("latest", reports$filename)), ]
reports <- reports[!(grepl("national.csv", reports$filename)), ]
a <- gsub("[A-z \\.\\(\\)]", "", reports$filename)
reports$filename <- substr(a, nchar(a)-4, nchar(a))
reports <- reports %>% rename(dag = filename)

# Plot
# Select all weekend days
weekends <- data.frame(xstart = unique(reports$Datum[as.numeric(wday(reports$Datum, label = TRUE)) == 7] - 0.2),
                       xend   = unique(reports$Datum[as.numeric(wday(reports$Datum, label = TRUE)) == 7] + 1.2) )

# Plot all reports together
reports %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden")),
         dag = factor(dag, sort(as.character(unique(reports$dag))))
  ) %>%
  ggplot(aes(x = Datum, y = Aantal, group = interaction(dag, Type), colour = Type)) +
  geom_line(aes(alpha = dag))+
  annotate("rect", xmin = weekends$xstart, xmax = weekends$xend, ymin = 0, ymax = max(reports$Aantal, na.rm = T), fill = "lightgray",
           alpha = .3) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  guides(alpha = FALSE)+
  ggtitle("Gerapporteerde COVID-19 patiënten per rapportagedatum")+
  ggsave("plots/overview_reports.png", width = 5.5, height=4)

#############
# plot geslacht

read_csv("data/rivm_NL_covid19_sex.csv") %>%
  filter(Geslacht %in% c("Man", "Vrouw")) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype= Geslacht)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per geslacht") +
  ggsave("plots/overview_plot_geslacht.png", width = 5.5, height=4)



# plot age

read_csv("data/rivm_NL_covid19_age.csv") %>%
  filter(LeeftijdGroep != "Niet vermeld") %>%
  mutate(
    groep = ifelse(LeeftijdGroep %in% c("0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59"), "0-59", NA),
    groep = ifelse(LeeftijdGroep %in% c("60-64", "65-69", "70-74"), "60-74", groep),
    groep = ifelse(LeeftijdGroep %in% c("75-79", "80-84", "85-89", "90-94", "95+"), "75+", groep)
  ) %>%
  group_by(Datum, groep, Type) %>%
  summarize(Aantal = sum(Aantal)) %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype=groep)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("COVID-19 patiënten per leeftijd") +
  ggsave("plots/overview_plot_leeftijd.png", width = 5.5, height=4)




# plot tests

read_csv("data/rivm_NL_covid19_tests.csv") %>%
  group_by(Datum, Type) %>%
  summarise(Aantal = max(Aantal)) %>%
  mutate(
    Type = if_else(Type == "Totaal", "Totaal testen", "Positieve testen")
  ) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
    geom_line() +
    theme_minimal() +
    theme(axis.title.x=element_blank(),
          axis.title.y=element_blank(),
          legend.pos = "bottom",
          legend.title = element_blank()) +
    scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
    scale_y_continuous(limits=c(0, NA)) +
    ggtitle("Totaal (positieve) COVID-19 testen") +
    ggsave("plots/overview_plot_tests.png", width = 5.5, height=4)


read_csv("data/rivm_NL_covid19_tests.csv") %>%
  group_by(Datum, Type) %>%
  summarise(Aantal = max(Aantal)) %>%
  ungroup() %>%
  pivot_wider(names_from = Type, values_from = Aantal) %>%
  mutate(
    `Positieve testen` = Positief - lag(Positief),
    `Totaal testen` = Totaal - lag(Totaal),
  ) %>%
  pivot_longer(c("Totaal testen", "Positieve testen"), names_to = "Type", values_to="Aantal", values_drop_na=T) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename (positieve) COVID-19 testen") +
  ggsave("plots/overview_plot_tests_diff.png", width = 5.5, height=4)








# plot with countermeasures

(daily %>%
  ggplot(aes(x = Datum, y = Aantal, colour = meas)) +
  geom_line() +
  scale_x_date(
    date_labels = "%d-%m-%Y",
    date_breaks = "1 weeks",
    date_minor_breaks = "1 days") +
  geom_rect(aes(xmin = start_datum,
                xmax = verwachtte_einddatum,
                ymin = -Inf,
                ymax = -0.025 * max(data_daily$Aantal, na.rm = TRUE),
                fill = name),
            inherit.aes = FALSE, data = measures) +
  geom_rug(aes(x = start_datum), inherit.aes = FALSE, data = measures) +
  coord_cartesian(xlim = c(min(data_daily$Datum), max(data_daily$Datum))) +
  scale_fill_viridis_d("Maatregel", guide = guide_legend(direction = "vertical")) +
  scale_colour_discrete("", guide = guide_legend(direction = "vertical")) +
  ggtitle("Aantal positief-geteste Coronavirus besmettingen in Nederland") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.key.size = unit(1, "mm"),
        legend.text = element_text(size = 6)) +
  ggsave("plots/timeline.png", width = 6, height=4))

### Top 10 municipalities
#
# # top 10 municipalities on the most recent day
# top_10_municipalities <- data %>%
#   filter(!is.na(Gemeentenaam)) %>%
#   arrange(desc(Datum), desc(Aantal)) %>%
#   filter(Gemeentenaam %in% head(Gemeentenaam, 10))
#
# # make plot
# top_10_municipalities %>%
#   ggplot(aes(Datum, Aantal, color=Gemeentenaam)) +
#   geom_line() +
#   theme_minimal() +
#   scale_x_date(date_breaks = "1 weeks",
#                date_minor_breaks = "1 days") +
#   theme(axis.title.x=element_blank(),
#         axis.title.y=element_blank()) +
#   ggtitle("Gemeentes met de meeste positief-geteste Coronavirus besmettingen") +
#   ggsave("plots/top_municipalities.png", width = 6, height=4)

### Per province
data_prov %>%
  filter(Datum == max(Datum), !is.na(Provincienaam)) %>%
  mutate(Provincie = forcats::fct_reorder(
    Provincienaam, Aantal, .fun = sum, .desc = TRUE)) %>%
  ggplot(aes(Provincie, Aantal)) +
  geom_col() +
  theme_minimal() +
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1.1)) +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  labs(title = "Positief-geteste Coronavirus besmettingen per provincie") +
  ggsave("plots/province_count.png", width = 6, height=4)

data_prov %>%
  ggplot(aes(Datum, Aantal, color=Provincienaam)) +
  geom_line() +
  theme_minimal() +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  labs(title = "Positief-geteste Coronavirus besmettingen per provincie") +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggsave("plots/province_count_time.png", width = 6, height=4)


### Model fits

## plots
data_daily_ext <- data_daily %>%
  # add some new rows for which we wish to predict the values
  bind_rows(tibble(Datum = seq(max(.$Datum) + 1, max(.$Datum) + 3, 1))) %>%
  arrange(Datum)

exponential.model <- lm(log(Aantal + 1) ~ Datum, data = filter(data_daily_ext, Aantal > 200))
summary(exponential.model)

pred <- cbind(data_daily_ext,
              exp(predict(exponential.model,
                          newdata = list(Datum = data_daily_ext$Datum),
                          interval = "confidence"))) %>%
  mutate(new = Aantal - lag(Aantal),
         growth = new / lag(new),
         # Vincent rescaled to -1 and 1 first
         ds = scales::rescale(Datum, to = c(-1, 1)),
         as = scales::rescale(Aantal, to = c(-1, 1)))

# NOTE: this plot is currently not used, as it is the same as what is done in Python currently
# try to find the inflection point of the sigmoidal fit
pred %>%
  mutate(new = Aantal - lag(Aantal),
         growth = new / lag(new)) %>%
  ggplot(aes(x = Datum, y = growth)) +
  geom_point() +
  geom_smooth(method = "lm") +
  geom_hline(yintercept = 1) +
  ggtitle("Groeisnelheid van positief-geteste Corona besmettingen in Nederland") +
  theme_minimal() +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggsave("plots/growth_rate_time.png", width = 6, height=4)

pred %>%
  ggplot(aes(Datum, Aantal)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = .2, fill = "red") +
  geom_line(aes(y = fit), colour = "red") +
  # only points for future dates?
  geom_point(aes(y = fit), colour = "red") +
  geom_line() +
  geom_point() +
  ylim(0, NA) +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  labs(title = "Aantal positief-geteste Coronavirus besmettingen",
       subtitle = "met exponentiële groei model voor >200 besmettingen") +
  ggsave("plots/prediction.png", width = 6, height=4)

pred %>%
  ggplot(aes(Datum, Aantal)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = .2, fill = "red") +
  geom_line(aes(y = fit), colour = "red") +
  # only points for future dates?
  geom_point(aes(y = fit), colour = "red",
             data = filter(pred, Datum > max(data_daily$Datum))) +
  geom_line() +
  geom_point() +
  scale_y_log10() +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  labs(title = "Aantal positief-geteste Coronavirus besmettingen",
       subtitle = "met exponentiële groei model voor >200 op een logaritmische schaal") +
  ggsave("plots/prediction_log10.png", width = 6, height=4)

# maps
library(sf)

# download province shapefile data
province_shp <- st_read("ext/NLD_adm/NLD_adm1.shp") %>%
  filter(ENGTYPE_1=="Province") %>%
  select(NAME_1)

plot(province_shp)

mun <- read_csv2(
  "ext/Gemeenten_alfabetisch_2019.csv",
  col_types = cols(Gemeentecode = "i")
)

# plot map

p_list = list()

data_map = data_prov %>%
  filter(!is.na(Provincienaam)) %>%
  complete(Datum, Provincienaam, fill = list("Aantal"=0)) %>%
  left_join(province_shp, by=c("Provincienaam"="NAME_1")) %>%
  st_as_sf() %>%
  st_set_crs(4326)

for (i in seq(0, 6)){
  print(i)
  data_subset_map = data_map %>%
    filter(Datum == max(Datum) - i*7)

  date_submap = max(data_subset_map$Datum)
  aantal_max = max(data_map$Aantal)

  p = data_subset_map %>%
    ggplot() +
    geom_sf(aes(fill=Aantal, color=Aantal, geometry = geometry)) + coord_sf( expand = FALSE) +
    theme_minimal() +
    theme(panel.grid.major = element_line(colour = "transparent"),
          axis.text.x=element_blank(),
          axis.text.y=element_blank(),
          plot.title = element_text(size = 8, hjust = 0.5)) +
    scale_colour_gradient(low = "grey", high = "#E69F00", na.value = NA, limits=c(0, aantal_max)) +
    scale_fill_gradient(low = "grey", high = "#E69F00", na.value = NA, limits=c(0, aantal_max))

  if (i == 0){
    p = p + ggtitle(date_submap)
    legend <- get_legend(
      # create some space to the left of the legend
      p + theme(legend.box.margin = margin(0, 0, 0, 12))
    )
    print(legend)
  } else if (i == 1) {
    p = p + ggtitle("-1 week")
  } else{
    p = p + ggtitle(glue("-{i} weken"))
  }

  p = p + theme(legend.position="none")

  p_list[[i+1]] = p
}

p_list[[8]] = legend

print("make grid plot")
pgrid = plot_grid(plotlist=p_list,
                  ncol=4) +
  ggsave("plots/map_province.png", width = 6, height=4)
