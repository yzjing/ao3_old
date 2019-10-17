library(mgcv)
df <- read.csv(file='/Users/a307/Desktop/work/current/ao3/exps/20190319_results_generation/fanfic_regression_data_merged_chs_rgam.tsv', header=TRUE, sep='\t')

df_kudos <- df[df$Kudos != 0, ]
 res_kudos <- mgcv::bam(Kudos ~ s(Term_novelty, bs='cr', sp=0.1,k=7) + s(Topic_novelty, bs='cr', sp=0.1,k=5) + s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+  Freq_relationship, data=df_kudos, method='REML', family='gaussian')

df_hits <- df[df$Hits != 0, ]
 res_hits <- mgcv::bam(Hits ~ s(Term_novelty, bs='cr', sp=0.1,k=7) + s(Topic_novelty, bs='cr', sp=0.1,k=5) + s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+ Freq_relationship , data=df_hits, method='REML', family='gaussian')

df_comments <- df[df$Comments != 0, ]
res_comments <- mgcv::bam(Comments ~ s(Term_novelty, bs='cr', sp=0.1,k=7) + s(Topic_novelty, bs='cr', sp=0.1,k=5) + s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+ Freq_relationship, data=df_comments, method='REML', family='gaussian')

df_bookmarks <- df[df$Bookmarks != 0, ]
 res_bookmarks <- mgcv::bam(Hits ~ s(Term_novelty, bs='cr', sp=0.1,k=7) + s(Topic_novelty, bs='cr', sp=0.1,k=5) + s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') 
+ Freq_relationship, data=df_bookmarks, method='REML', family='gaussian')


pdf('/Users/a307/Desktop/gam_res.pdf', width=16, height=8)
par(mfrow=c(2,4))
plot(res_kudos, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Kudos', cex.lab=1.6, cex.axis=2)
plot(res_hits, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Hits', cex.lab=1.6, cex.axis=2)
plot(res_comments, scale=0, shade=TRUE,  select=1, xlab='Term novelty', ylab='Comments', cex.lab=1.6, cex.axis=2)
plot(res_bookmarks, scale=0, shade=TRUE, select=1, xlab='Term novelty', ylab='Bookmarks', cex.lab=1.6, cex.axis=2)
plot(res_kudos, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Kudos', cex.lab=1.6, cex.axis=2)
plot(res_hits, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Hits', cex.lab=1.6, cex.axis=2)
plot(res_comments, scale=0, shade=TRUE,  select=2, xlab='Topic novelty', ylab='Comments', cex.lab=1.6, cex.axis=2)
plot(res_bookmarks, scale=0, shade=TRUE, select=2, xlab='Topic novelty', ylab='Bookmarks', cex.lab=1.6, cex.axis=2)
dev.off()
        


# produce results like the previous ones 
# res <- mgcv::gam(Kudos ~ s(Term_novelty, bs='cr', sp=0.8, k=12) + s(Topic_novelty, bs='cr', sp=0.8, k=12), data = df)

#family = 'nb' is better than default


