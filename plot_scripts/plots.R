library(tidyverse)

pdf(NULL)
dir.create("plots")

data <- read_csv("data/rivm_corona_in_nl.csv")
data_daily <- read_csv("data/rivm_corona_in_nl_daily.csv")
measures <- read_csv("ext/maatregelen.csv")

data_daily %>%
  ## add_row(Datum = "2020-02-26", Aantal = 0) %>%
  ggplot(aes(Datum, Aantal)) +
  geom_line() +
  geom_text(x = lubridate::today(), y = Inf, vjust = 1, size = 3.5,
            label = paste("Vandaag:", format(lubridate::today(), "%d-%m-%Y"))) +
  coord_cartesian(
    ylim = c(0, max(data_daily$Aantal, na.rm = TRUE)),
    xlim = c(min(data_daily$Datum, na.rm = TRUE), lubridate::today() + 3)) +
  scale_x_date(
    date_labels = "%d-%m-%Y",
    date_breaks = "1 weeks",
    date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
    geom_rect(aes(xmin = start_datum,
                xmax = verwachtte_einddatum,
                ymin = -Inf,
                ymax = -0.025 * max(data_daily$Aantal, na.rm = TRUE),
                fill = maatregel), inherit.aes = FALSE,
            alpha = 0.5, data = measures) +
  geom_rug(aes(x = start_datum, y = NULL), data = measures) +
  geom_vline(xintercept = lubridate::today(), colour = "red") +
  geom_text(aes(x = start_datum, label = maatregel, y = -Inf),
            size = 3.5, angle = 10, vjust = -4, hjust = 0, data = measures) +
  scale_fill_viridis_d(guide = FALSE) +
  ggtitle("Aantal positief-geteste Coronavirus besmettingen in Nederland") +
  ggsave("plots/timeline.png", width = 6, height=4)

### Top 10 municipalities

# top 10 municipalities on the most recent day
top_10_municipalities <- data %>%
  filter(!is.na(Gemeentenaam)) %>%
  arrange(desc(Datum), desc(Aantal)) %>%
  head(10) %>%
  select(Gemeentenaam)

# make plot
data %>%
  filter(!is.na(Gemeentenaam)) %>%
  inner_join(top_10_municipalities) %>%
  complete(Gemeentenaam, Datum, fill=list("Aantal"=0)) %>%
  arrange(desc(Datum), desc(Aantal)) %>%
  mutate(Gemeentenaam = factor(Gemeentenaam, levels=pull(top_10_municipalities, Gemeentenaam))) %>%
  ggplot(aes(Datum, Aantal, color=Gemeentenaam)) +
  geom_line() +
  theme_minimal() +
  scale_x_date(date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  geom_vline(xintercept = lubridate::today(), colour = "red") +
  coord_cartesian(
    xlim = c(min(data_daily$Datum, na.rm = TRUE), lubridate::today() + 3)) +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Gemeentes met de meeste positief-geteste Coronavirus besmettingen") +
  ggsave("plots/top_municipalities.png", width = 6, height=4)

### Per province

data %>%
  filter(Datum == max(Datum), !is.na(Gemeentenaam)) %>%
  ggplot(aes(Provincienaam, Aantal)) +
  geom_col() +
  theme_minimal() +
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1.1)) +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Positief-geteste Coronavirus besmettingen per provincie") +
  ggsave("plots/province_count.png", width = 6, height=4)

data %>%
  filter(!is.na(Gemeentenaam)) %>%
  group_by(Provincienaam, Datum) %>%
  summarise(Aantal = sum(Aantal, na.rm = T)) %>%
  ggplot(aes(Datum, Aantal, color=Provincienaam)) +
  geom_line() +
  theme_minimal() +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  coord_cartesian(
    xlim = c(min(data$Datum, na.rm = TRUE), lubridate::today() + 3)) +
  geom_vline(xintercept = lubridate::today(), colour = "red") +
  ggtitle("Positief-geteste Coronavirus besmettingen per provincie") +
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
  geom_vline(xintercept = lubridate::today(), colour = "red") +
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
  geom_point(aes(y = fit), colour = "red",
             data = filter(pred, Datum > max(data_daily$Datum))) +
  geom_line() +
  geom_vline(xintercept = lubridate::today(), colour = "red") +
  geom_point() +
  ylim(0, NA) +
  ## scale_y_log10() + # also cool to see how it's already deviating from the line!
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Aantal positief-geteste Coronavirus besmettingen met exponentiële groei model") +
  ggsave("plots/prediction.png", width = 6, height=4)

pred %>%
  ggplot(aes(Datum, Aantal)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = .2, fill = "red") +
  geom_line(aes(y = fit), colour = "red") +
  # only points for future dates?
  geom_point(aes(y = fit), colour = "red",
             data = filter(pred, Datum > max(data_daily$Datum))) +
  geom_line() +
  geom_vline(xintercept = lubridate::today(), colour = "red") +
  geom_point() +
  scale_y_log10() +
  scale_x_date(date_labels = "%d-%m-%Y",
               date_breaks = "1 weeks",
               date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Aantal positief-geteste Coronavirus besmettingen met exponentiële groei model op een logaritmische schaal") +
  ggsave("plots/prediction_log10.png", width = 6, height=4)

# maps
library(sf)

# download province shapefile data
province_shp <- st_read("ext/NLD_adm/NLD_adm1.shp") %>%
  filter(ENGTYPE_1=="Province") %>%
  select(NAME_1)

mun <- read_csv2(
  "ext/Gemeenten_alfabetisch_2019.csv",
  col_types = cols(Gemeentecode = "i")
)

# plot map
province_data <- data %>%
  filter(!is.na(Gemeentenaam)) %>%
  group_by(Datum, Provincienaam) %>%
  summarise(Aantal = sum(Aantal, na.rm = T)) %>%
  ungroup() %>%
  left_join(province_shp, by=c("Provincienaam"="NAME_1"))


province_data %>%
  filter(Datum > max(Datum) - 3) %>%
  ggplot() +
  geom_sf(aes(fill=Aantal, color=Aantal, geometry = geometry)) +
  facet_grid(cols = vars(Datum)) +
  theme_minimal() +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank()) +
  scale_colour_gradient(low = "grey", high = "red", na.value = NA) +
  scale_fill_gradient(low = "grey", high = "red", na.value = NA) +
  ggsave("plots/map_province.png", width = 6, height=2)
