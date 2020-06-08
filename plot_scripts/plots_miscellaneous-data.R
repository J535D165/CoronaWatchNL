library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

##############################
##### MISCELLANEOUS DATA #####
##############################

### TEST DATA

# Tests: Toename per kalender week (einde van de week (zondag) als plotdatum)
test <- read_csv("data-misc/data-test/RIVM_NL_test_latest.csv")

test %>%
  mutate(
    Type = if_else(Type == "Totaal", "Totaal testen", "Positieve testen")
  ) %>%
  ggplot(aes(x = EindDatum, y = Aantal, colour = Type)) +
  geom_line()+
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Toename totaal (positieve) COVID-19 testen per week") +
  ggsave("plots/overview_plot_tests_weeks.png", width = 5.5, height=4)
  
# Tests: Cumulatief per kalender week (einde van de week (zondag) als plotdatum)
test %>%
  filter(Type == "Totaal") %>%
  mutate(Cumulatief = cumsum(Aantal)) %>%
  bind_rows(test %>%
              filter(Type == "Positief") %>%
              mutate(Cumulatief = cumsum(Aantal))) %>%
  mutate(
    Type = if_else(Type == "Totaal", "Totaal testen", "Positieve testen")
  ) %>%
  ggplot(aes(x = EindDatum, y = Cumulatief, colour = Type)) +
  geom_line() +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  ggtitle("Totaal (positieve) COVID-19 testen per week") +
  ggsave("plots/overview_plot_tests_weeks_cum.png", width = 5.5, height=4)


# Tests: oude data (tm 19 april) totaal (positive) tests
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

# Tests: Toename (positieve) testen
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


### UNDERLYING CONDITIONS 
con  <- read_csv("data-misc/data-underlying/data-underlying_conditions/RIVM_NL_deceased_under70_conditions.csv")
stat <- read_csv("data-misc/data-underlying/data-underlying_statistics/RIVM_NL_deceased_under70_statistics.csv") 

con$Type[which(con$Type == "Chronische neurologische of neuromusculaire aandoeningen")] <- "Chronisch neurologisch/neuromusculair"

con %>%
  filter(Type != "Overig") %>%
  mutate(Type = factor(Type, c("Cardio-vasculair en hypertensie", "Diabetes", "Chronische longaandoeningen", "Maligniteit", "Chronisch neurologisch/neuromusculair", "Nieraandoening", "Leveraandoening", "Immuundeficientie", "Zwangerschap"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type)) +
  geom_line() +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.text = element_text(size = 7)) +
  ggtitle("Onderliggende aandoeningen en/of zwangerschap van overledenen (<70 jaar)")+
  labs(subtitle = "Cumulatief van gevonden onderliggende aandoeningen en/of zwangerschap bij overleden 
       COVID-19 patienten onder de 70 jaar") +
  ggsave("plots/underlying_conditions.png", width = 8.5, height=4)

stat %>%
  mutate(Type = factor(Type, c("Totaal gemeld", "Onderliggende aandoening en/of zwangerschap", "Niet vermeld", "Geen onderliggende aandoening"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type)) +
  geom_line() +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.text = element_text(size = 9)) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999", "gray")) +
  ggtitle("Aantal overledenen (<70 jaar) met onderliggende aandoeningen en/of zwangerschap")+
  labs(subtitle = "Cumulatief aantal overleden COVID-19 patienten onder de 70 jaar met onderliggende 
       aandoeningen en/of zwangerschap") +
  ggsave("plots/conditions_statistics.png", width = 8.5, height=4)


### Reproduction index
rep <- read_csv("data-misc/data-reproduction/RIVM_NL_reproduction_index.csv")

rep2 <- spread(rep, Type, Aantal)

rep2 %>%
  ggplot(aes(x= Datum, y = `Reproductie index`)) +
  geom_line(aes(y = `Reproductie index`)) +
  geom_ribbon(aes(ymin = Minimum, ymax = Maximum), fill="#E69F00", alpha=.5) +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.text = element_text(size = 9)) +
  ggtitle("Reproductie index per dag") +
  ggsave("plots/reproductie_index.png", width = 5.5, height=4)

