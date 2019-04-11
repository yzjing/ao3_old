library(mgcv)
df <- read.csv(file='/Users/a307/Desktop/work/current/ao3/exps/20190319_results_generation/fanfic_regression_data_curated.tsv', header=TRUE, sep='\t')

res <- mgcv::bam(Kudos ~ s(Term_novelty, bs='cr', sp=0.0001, k=20) + s(Topic_novelty, bs='cr', sp=0.0001, k=20) + s(Chapters, sp=0.1, bs='cr') + s(author_fic_cnt, sp=0.1, bs='cr') + s(History, sp=0.1, bs='cr') + s(Words, sp=0.1, bs='cr')
+  + Freq_relationship + Category_F_F + Category_F_M + Category_Gen + Category_M_M
+  + Category_Multi + Category_Other + ArchiveWarnings_underage + ArchiveWarnings_death + 
+ ArchiveWarnings_choose_no + ArchiveWarnings_no_apply + ArchiveWarnings_violence + Rating_E                  
+ + Rating_G + Rating_M + Rating_N + Fandom_harry_potter + Fandom_dcu + Fandom_doctor_who + Fandom_star_wars          
+ + Fandom_arthurian + Fandom_supernatural + Fandom_haikyuu  + Fandom_kuroko_no_basuke + Fandom_hamilton_miranda 
+ + Fandom_dragon_age + Fandom_the_walking_dead + Fandom_buffy  + Fandom_les_miserables + Fandom_naruto + Fandom_tolkien 
+ +  Fandom_shakespare + Fandom_hetalia + Fandom_attack_on_titan + Fandom_ms_paint_adventures + Fandom_marvel             
+ + Fandom_sailor_moon+ Fandom_one_direction, data=df, method='REML', family='scat')




     
  
                
        


# produce results like the previous ones 
# res <- mgcv::gam(Kudos ~ s(Term_novelty, bs='cr', sp=0.8, k=12) + s(Topic_novelty, bs='cr', sp=0.8, k=12), data = df)

#family = 'nb' is better than default


