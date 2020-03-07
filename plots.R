library(tidyverse)

dir.create("plots")

data = read_csv("data/rivm_corona_in_nl.csv")

data %>%
  group_by(Datum) %>%
  summarise(Aantal=sum(Aantal, na.rm = T)) %>%
  ggplot(aes(Datum, Aantal)) +
    geom_line() + 
    ylim(0, NA) + 
    # xlim(as.Date("2020-02-27"), NA) + 
    theme_minimal() + 
    ggtitle("Aantal positieve testen op Corona") + 
    ggsave("plots/timeline.png", width = 6, height=4)


### Top 10 municipalities

# top 10 municipalities on the most recent day
top_10_municipalities = data %>% 
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
    ggtitle("Top 10 gemeentes met meeste corona besmettingen") + 
    ggsave("plots/top_municipalities.png", width = 6, height=4)
