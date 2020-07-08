library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

#############################
##### GEOGRAPHICAL DATA #####
#############################

##################
## INZICHT DATA ##
##################

# TOTAAL COVID-19 PATIENTEN #
read_csv("data/rivm_NL_covid19_national.csv") %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Totaal COVID-19 patiënten") +
  ggsave("plots/overview_plot.png", width = 5.5, height=4)


# TOENAME COVID-19 PATIENTEN #
# load data
data_national <- read_csv("data/rivm_NL_covid19_national.csv")

# mutate and combine datasets
daily_diff <- data_national %>%
  filter(Type == "Totaal") %>%
  mutate(
    Aantal = Aantal - lag(Aantal),
  ) %>%
  bind_rows(data_national %>%
              filter(Type == "Ziekenhuisopname") %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
              )
  ) %>%
  bind_rows(data_national %>%
              filter(Type == "Overleden") %>%
              mutate(
                Aantal = Aantal - lag(Aantal),
              )
  )

# plot toename COVID-19 patienten
daily_diff %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename COVID-19 patiënten") +
  ggsave("plots/overview_plot_diff.png", width = 5.5, height=4)


####################################
### NEWLY REPORTED VS. WERKELIJK ###
####################################

# TOENAME COVID-19 PATIENTEN #
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
        legend.title = element_blank(),
        legend.text = element_text(size = 8)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Toename: Werkelijk vs. Gerapporteerd") +
  ggsave("plots/overview_plot_true_vs_reported_diff.png", width = 5.5, height=4)


# TOENAME COVID-19 PATIENTEN #
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
        legend.title = element_blank(),
        legend.text = element_text(size = 8)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9","#999999")) +
  ggtitle("Totaal: Werkelijk vs. Gerapporteerd") +
  ggsave("plots/overview_plot_true_vs_reported.png", width = 5.5, height=4)



#############################
#### NUMBERS PER REPORT #####
#############################

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
  labs(caption = 'Vanaf 1 juli wordt er een rapport per week i.p.v. per dag gepubliceerd') +
  geom_vline(xintercept=as.Date('2020-07-01'), linetype = 2, color = 'gray') +
  ggtitle("Gerapporteerde COVID-19 patiënten per rapportagedatum")+
  ggsave("plots/overview_reports.png", width = 5.5, height=4)


#####################
### PROVINCE DATA ###
#####################

# load province data
data_prov <- read_csv("data/rivm_NL_covid19_province.csv")

# Positief-geteste Coronavirus besmettingen per provincie
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

# Positief-geteste Coronavirus besmettingen per provincie
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


#####################
######## MAPS #######
#####################
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



#####################
####### REMARKS #####
#####################


df_report_diff = samen_cum %>% 
  spread(Type, Aantal) %>% 
  mutate(
    meas = factor(meas, c("Totaal", "Ziekenhuisopname", "Overleden")),
    Onzichtbaar = Werkelijk - Gerapporteerd) 

df_report_diff %>% 
  ggplot(aes(x = Datum, y = Onzichtbaar, group = interaction(meas), colour = meas))+
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        legend.text = element_text(size = 8),
        title = element_text(size = 10)
  ) +
  scale_color_manual(values=c("#E69F00", "#56B4E9","#999999")) +
  ggtitle(
    label="Rapportageachterstand bij rapportage aan het RIVM",
    subtitle="Het verschil tussen het (voorlopige) totaal aantal patienten op de betreffende dag en het \ntotaal gemeld op die dag door het RIVM."
  ) +
  ggsave("plots/remarks_plot_rapportageachterstand.png", width = 5.5, height=4)


read_csv("data-geo/data-municipal/RIVM_NL_municipal.csv") %>% 
  filter(Gemeentenaam == "Tilburg",
         Datum < "2020-05-01") %>% 
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname", "Overleden"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type)) +
  geom_line() +
  geom_vline(xintercept = as.Date("2020-03-31")) + 
  geom_vline(xintercept = as.Date("2020-04-08")) + 
  geom_vline(xintercept = as.Date("2020-04-18")) + 
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Totaal aantal COVID-19 patiënten in Tilburg") +
  ggsave("plots/remarks_plot_tilburg.png", width = 5.5, height=4)

