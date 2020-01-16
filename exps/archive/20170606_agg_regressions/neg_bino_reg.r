libraty(MASS)
df = read.csv('/Users/jingy/Desktop/ao3/exps/20170606_negative_binomial_reg/regression_data.csv')
summary(m1 <- glm.nb(Kudos ~ Bookmarks + Chapters + Hits + Words + Comments + PublishDate + Cosine_distance, data = df))