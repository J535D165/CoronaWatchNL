library(tidyverse)

pdf(NULL)
dir.create("plots")

data <- read_csv("data/rivm_corona_in_nl.csv")
data_daily <- read_csv("data/rivm_corona_in_nl_daily.csv")

data_daily %>%
  add_row(Datum = "2020-02-26", Aantal = 0) %>%
  ggplot(aes(Datum, Aantal)) +
  geom_line() +
  ylim(0, NA) +
  scale_x_date(
    breaks = seq(lubridate::ymd("2020-02-26"), lubridate::today(),
                 by = "1 week"),
    date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Aantal Coronavirus besmettingen") +
  ggsave("plots/timeline.png", width = 6, height=4)


### Top 10 municipalities

# top 10 municipalities on the most recent day
top_10_municipalities <- data %>%
  arrange(desc(Datum), desc(Aantal)) %>%
  head(10) %>%
  select(Gemeente)

# make plot
data %>%
  inner_join(top_10_municipalities) %>%
  complete(Gemeente, Datum, fill=list("Aantal"=0)) %>%
  arrange(desc(Datum), desc(Aantal)) %>%
  mutate(Gemeente = factor(Gemeente, levels=pull(top_10_municipalities, Gemeente))) %>%
  ggplot(aes(Datum, Aantal, color=Gemeente)) +
  geom_line() +
  theme_minimal() +
  scale_x_date(
    breaks = seq(lubridate::ymd("2020-02-26"), lubridate::today(),
                 by = "1 week"),
    date_minor_breaks = "1 days") +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Gemeentes met meeste Coronavirus besmettingen") +
  ggsave("plots/top_municipalities.png", width = 6, height=4)

### Per province

mun = read_csv2(
  "ext/Gemeenten_alfabetisch_2019.csv",
  col_types = cols(Gemeentecode = "i")
)

data %>% left_join(
  select(mun, Gemeentecode, Provincienaam),
  by=c("id"="Gemeentecode")
) %>%
  filter(Datum == max(Datum)) %>%
  ggplot(aes(Provincienaam, Aantal)) +
  geom_col() +
  theme_minimal() +
  theme(axis.text.x=element_text(angle=45,hjust=1,vjust=1.1)) +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggtitle("Coronavirus besmettingen per provincie") +
  ggsave("plots/province_count.png", width = 6, height=4)

data %>%
  left_join(
    select(mun, Gemeentecode, Provincienaam),
    by=c("id"="Gemeentecode"))%>%
  group_by(Provincienaam, Datum) %>%
  summarise(Aantal = sum(Aantal, na.rm = T)) %>%
  ggplot(aes(Datum, Aantal, color=Provincienaam)) +
  geom_line() +
  theme_minimal() +
  scale_x_date(
    breaks = seq(lubridate::ymd("2020-02-26"), lubridate::today(),
                 by = "1 week"),
    date_minor_breaks = "1 days") +
  ggtitle("Coronavirus besmettingen per provincie") +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggsave("plots/province_count_time.png", width = 6, height=4)


### Predictions

## plots
data_daily_ext <- data_daily %>%
  # add initial number
  add_row(Datum = "2020-02-26", Aantal = 0) %>%
  # add some new rows for which we wish to predict the values
  bind_rows(tibble(Datum = seq(max(.$Datum) + 1, max(.$Datum) + 3, 1))) %>%
  arrange(Datum)

exponential.model <- lm(log(Aantal + 1) ~ Datum, data = data_daily_ext)
summary(exponential.model)

pred <- cbind(data_daily_ext,
              exp(predict(exponential.model,
                          newdata = list(Datum = data_daily_ext$Datum),
                          interval = "confidence")))

pred %>%
  ggplot(aes(Datum, Aantal)) +
  geom_ribbon(aes(ymin = lwr, ymax = upr), alpha = .2, fill = "red") +
  geom_line(aes(y = fit), colour = "red") +
  geom_point(aes(y = fit), colour = "red", data = filter(pred, Datum > max(data_daily$Datum))) +
  geom_line() +
  geom_point() +
  ylim(0, NA) +
  ## scale_y_log10() + # also cool to see how it's already deviating from the line!
  scale_x_date(
    breaks = seq(lubridate::ymd("2020-02-26"), lubridate::today(),
                 by = "1 week"),
    date_minor_breaks = "1 days") +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank())
  ggtitle("Voorspelling aantal Coronavirus besmettingen") +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank()) +
  ggsave("plots/prediction.png", width = 6, height=4)

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
  left_join(
    select(mun, Gemeentenaam, Provincienaam, GemeentecodeGM),
    by=c("Gemeente"="Gemeentenaam")
  ) %>%
  group_by(Datum, Provincienaam) %>%
  summarise(Aantal = sum(Aantal, na.rm = T)) %>%
  ungroup() %>%
  left_join(province_shp, by=c("Provincienaam"="NAME_1"))


province_data %>%
  filter(Datum > max(Datum) - 3) %>%
  ggplot() +
  geom_sf(aes(fill=Aantal, color=Aantal)) +
  facet_grid(cols = vars(Datum)) +
  theme_minimal() +
  theme(axis.text.x=element_blank(),
        axis.text.y=element_blank()) +
  scale_colour_gradient(low = "grey", high = "red", na.value = NA) +
  scale_fill_gradient(low = "grey", high = "red", na.value = NA) +
  ggsave("plots/map_province.png", width = 6, height=2)
