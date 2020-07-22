library(tidyverse)
library(cowplot)
library(glue)
library(lubridate)
dir.create("plots")

##############################
####### DASHBOARD DATA #######
##############################

### CONTAGIOUS DATA
# Contagious:
cont <- read_csv("data-dashboard/data-contagious/data-contagious_estimates/RIVM_NL_contagious_estimate.csv")

cont2 <- spread(cont, Type, Waarde)

cont2 %>%
  ggplot(aes(x= Datum, y = `Geschat aantal besmettelijke mensen`)) +
  geom_line(aes(y = `Geschat aantal besmettelijke mensen`)) +
  geom_ribbon(aes(ymin = `Minimum aantal besmettelijke mensen`, ymax = `Maximum aantal besmettelijke mensen`), fill="#E69F00", alpha=.5) +
  scale_y_continuous(limits=c(0, NA)) +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        legend.title = element_blank(),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.text = element_text(size = 9)) +
  ggtitle("Geschat aantal besmettelijke mensen") +
  labs(subtitle = "per 100.000 inwoners per dag") +
  ggsave("plots/contagious.png", width = 8.5, height=4)


### REPRODUCTION INDEX
# Reproduction index:
rep <- read_csv("data-dashboard/data-reproduction/RIVM_NL_reproduction_index.csv")

rep2 <- spread(rep, Type, Waarde)

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
  ggsave("plots/reproductie_index.png", width = 8.5, height=4)


### NURSERY HOME COUNTS
# Toename bewoners:
read_csv("data-dashboard/data-nursery/data-nursery_residents/RIVM_NL_nursery_residents.csv") %>%
  mutate(Type = factor(Type, c("Positief geteste bewoners", "Overleden besmette bewoners"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Toename (overleden) positief geteste verpleegtehuis bewoners") +
  ggsave("plots/overview_nursery_count.png", width = 5.5, height=4)

# Cumulatief bewoners:
read_csv("data-dashboard/data-nursery/data-nursery_residents/RIVM_NL_nursery_residents.csv") %>%
  mutate(Type = factor(Type, c("Positief geteste bewoners", "Overleden besmette bewoners"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Totaal (overleden) positief geteste verpleegtehuis bewoners") +
  ggsave("plots/overview_nursery_cumulative.png", width = 5.5, height=4)

# Totaal verpleeghuizen:
read_csv("data-dashboard/data-nursery/data-nursery_homes/RIVM_NL_nursery_counts.csv") %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Totaal aantal verpleegtehuizen met besmette bewoners") +
  ggsave("plots/overview_nursery_homes.png", width = 5.5, height=4)

# Nieuwe verpleeghuizen:
read_csv("data-dashboard/data-nursery/data-nursery_homes/RIVM_NL_nursery_counts.csv") %>%
  ggplot(aes(x = Datum, y = NieuwAantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Nieuw aantal verpleegtehuizen met besmette bewoners") +
  ggsave("plots/overview_nursery_homes_new.png", width = 5.5, height=4)


### SEWAGE
# Virusdeeltjes per ml:
read_csv("data-dashboard/data-sewage/RIVM_NL_sewage_counts.csv") %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Aantal virusdeeltjes per ml rioolwater per week") +
  ggsave("plots/overview_sewage.png", width = 5.5, height=4)


### SUSPECTS
# Verdachte patienten:
read_csv("data-dashboard/data-suspects/RIVM_NL_suspects.csv") %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Door huisarts gerapporteerde verdachte COVID-19 patiÃ«nten") +
  labs(subtitle = 'per 100.000 inwoners per week')
  ggsave("plots/overview_suspects.png", width = 5.5, height=4)

### CASES
# Cumulatief
read_csv("data-dashboard/data-cases/RIVM_NL_national_dashboard.csv") %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Totaal COVID-19 patiÃ«nten") +
  ggsave("plots/overview_national_dashboard.png", width = 5.5, height=4)

# Toename
read_csv("data-dashboard/data-cases/RIVM_NL_national_dashboard.csv") %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Toename COVID-19 patiÃ«nten") +
  ggsave("plots/overview_national_dashboard_new.png", width = 5.5, height=4)

# Cumulatief: Rapport vs. Dashboard
dash <- read_csv("data-dashboard/data-cases/RIVM_NL_national_dashboard.csv")
rap <- read_csv("data-geo/data-national/RIVM_NL_national.csv")

alles <- rap %>% filter(Type != 'Overleden') %>% mutate(meas = 'Rapport') %>% bind_rows(dash %>% mutate(meas = 'Dashboard'))

alles %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname"))) %>%
  mutate(meas = factor(meas, c("Dashboard", "Rapport"))) %>%
  ggplot(aes(x = Datum, y = AantalCumulatief, colour = Type, linetype = meas)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Totaal COVID-19 patiÃ«nten: Rapport vs. Dashboard") +
  ggsave("plots/overview_national_vs_dashboard.png", width = 5.5, height=4)

# Toename: Rapport vs. Dashboard
alles %>%
  mutate(Type = factor(Type, c("Totaal", "Ziekenhuisopname"))) %>%
  mutate(meas = factor(meas, c("Dashboard", "Rapport"))) %>%
  ggplot(aes(x = Datum, y = Aantal, colour = Type, linetype = meas)) +
  geom_line() +
  theme_minimal() +
  theme(axis.title.x=element_blank(),
        axis.title.y=element_blank(),
        legend.pos = "bottom",
        plot.title = element_text(hjust = 0.5),
        plot.subtitle=element_text(size=11, hjust=0.5),
        legend.title = element_blank()) +
  scale_color_manual(values=c("#E69F00", "#56B4E9", "#999999")) +
  scale_y_continuous(limits=c(0, NA)) +
  ggtitle("Toename COVID-19 patiÃ«nten: Rapport vs. Dashboard") +
  ggsave("plots/overview_national_vs_dashboard_new.png", width = 5.5, height=4)

