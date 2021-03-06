#
#
#              Generation of synthetic HS_Data for reconstruction, using leaf blade profiles per nff
#
source('1_HS_plantes_baguees.R')
source('2_Blade_length_profiles.R')
#
# tagged plants : regenerate HS data with leaf profiles
# -----------------------------------------------------
#
dimPMf <- lapply(LbM, function(Lb) do.call('rbind',lapply(names(Lb), function(nff) data.frame(nff=as.numeric(nff), rank = Lb[[nff]]$ranks, x=Lb[[nff]]$L))))
dimPMMf <- lapply(LbMM, function(Lb) {Lb$x=Lb$L;Lb$rank=Lb$ranks;Lb})
#
dimPfitf <- mapply(function(dim,name) do.call('rbind', lapply(split(dim, dim$N), function(mat) final_length(mat,dimPMf[[name]], dimPMMf[[name]]))), dimP, names(dimP), SIMPLIFY=FALSE)
# HS,SSI per plant
phendbf <- sapply(genos, function(g) pheno(tagged[[g]], dimPfitf[[g]]), simplify=FALSE)
#
# ajout estimation SSI terrain 27/04 Mercia/Rht3
#
SSIobsMercia <- data.frame(Date='27/04/2011', N=c(8,11), SSI=c(7.3, 8.2))
SSIobsRht3 <- data.frame(Date='27/04/2011', N=c(1,4,5,6,8,11), SSI=c(7.4, 6.3,6.2,7.1,7.4,6.2))
phendbf$Mercia$SSI[match(paste(SSIobsMercia$Date,SSIobsMercia$N),paste(as.character(phendbf$Mercia$Date), phendbf$Mercia$N))] <- SSIobsMercia$SSI
phendbf$Rht3$SSI[match(paste(SSIobsRht3$Date,SSIobsRht3$N),paste(as.character(phendbf$Rht3$Date), phendbf$Rht3$N))] <- SSIobsRht3$SSI
phendbf$Mercia$GL = phendbf$Mercia$HS - phendbf$Mercia$SSI
phendbf$Rht3$GL = phendbf$Rht3$HS - phendbf$Rht3$SSI
#check
par(mfrow=c(2,2),mar=c(4,4,1,1))
lapply(phendbf, function(p) {
  plot(c(0,2500),c(0,13),type='n')
  lapply(split(p,p$N), function(x) points(x$TT,x$HS,col=x$nff,pch=16))
  lapply(split(p,p$N), function(x) points(x$TT,x$GL,col=x$nff,pch=16))
})
#
# Export
#
write.csv(do.call('rbind', sapply(genos, function(g) {phen <- phendbf[[g]]; phen$label = g; phen[,c('Date', 'label', 'Trt', 'Rep', 'N', 'Axis', 'Nflig', 'Nfvis', 'nff', 'HS', 'SSI', 'GL')]}, simplify=FALSE)), 'Compil_Pheno_treated_archi_tagged.csv',row.names=FALSE)
#
# HS/SSI data from detructive samplings
# -------------------------------------
#
phend <- NULL
#scan samples Tremie 12
dat <- scanleafdb[scanleafdb$variety=='Tremie12' & as.character(scanleafdb$id_Axe)=='MB',]
phen <- do.call('rbind',lapply(split(dat,list(dat$prelevement,dat$N), drop=TRUE), function(x) pheno_scan(x, LbMM$Tremie12)))
phen <- merge(phen, TTlin$Tremie12)
phend$Tremie12 <- phen
#scan samples Tremie13
dat <- scanleafdb[scanleafdb$variety=='Tremie13' & as.character(scanleafdb$id_Axe)=='MB',]
dat$lmax <- sqrt(dat$A_bl)#proxy for pheno_scan input
phen <- do.call('rbind',lapply(split(dat,list(dat$prelevement,dat$N), drop=TRUE), function(x) pheno_scan(x, LbMM$Tremie13)))
phen <- merge(phen, TTlin$Tremie13)
phend$Tremie13 <- phen
# SSI, GL from silhouette data Tremie12 12/06/12
dat <- notdb$Tremie12$sampled_plants_120612[,1:9]
dat <- dat[dat$axe=='MB',]
phen <- data.frame(Source='sampled_plants_120612',Date=dat$Date, N=dat$N, nff=dat$Nflig, Nflig=dat$Nflig, Nfvis=0, HS=dat$Nflig, SSI=dat$Nflig - dat$Nfvert, GL=dat$Nfvert)
phen <- merge(phen, TTlin$Tremie12)
phend$Tremie12 <- rbind(phend$Tremie12, phen)
# ssi sample Tremie13 02/04/2013
dat <- notdb$Tremie13$sampled_plants_020413
dat$Source='sampled_plants_020413'
dat$Nflig <- NA
dat$Nfvis <- NA
phen <- pheno_ssi(dat)[,c('Source','Date', 'N','nff','Nflig', 'Nfvis', 'HS','SSI','GL','TT')]
phend$Tremie13 <- rbind(phend$Tremie13, phen)
# HS from silhouette data Tremie13 29/04
dat <- curvdb$Tremie13[curvdb$Tremie13$Source=='sampled_plants_290413',]
dat <- HcLbCurv(dat)
dat <- merge(dat,leafcdb$Tremie13[leafcdb$Tremie13$Source=='sampled_plants_290413',])
dat$lmax <- dat$Lb
dat$stat=1
dat$prelevement <- sapply(as.character(dat$Source), function(s) format(as.Date(strsplit(s,split='_')[[1]][3], '%d%m%y'),'%d/%m/%Y'))
dat$A_bl_green <- NA
dat$A_bl <- NA
phen <- do.call('rbind',lapply(split(dat,list(dat$prelevement,dat$N), drop=TRUE), function(x) pheno_scan(x, LbMM$Tremie13)))
phen <- merge(phen, TTlin$Tremie13)
phend$Tremie13 <- rbind(phend$Tremie13, phen)
#
#check
par(mfrow=c(2,2),mar=c(4,4,1,1))
lapply(names(phendbf), function(g) {
  p <- phendbf[[g]]
  plot(c(0,2500),c(0,14),type='n')
  lapply(split(p,p$N), function(x) points(x$TT,x$HS,col=x$nff,pch=16))
  lapply(split(p,p$N), function(x) points(x$TT,x$SSI,col=x$nff,pch=16,cex=0.7))
  lapply(split(p,p$N), function(x) points(x$TT,x$GL,col=x$nff,pch=16))
  if (g %in% names(phend)){
    phen <- phend[[g]]
    coul <- ifelse(is.na(phen$nff),8,nff)
    symb <- ifelse(is.na(phen$nff),16,1)
    points(phen$TT, phen$HS,pch=symb,col=coul)
    points(phen$TT, phen$SSI, pch=symb, col=coul,cex=0.7)
     points(phen$TT, phen$GL, pch=symb, col=coul)
  }
})
#
# Export
#
write.csv(do.call('rbind', sapply(names(phend), function(g) {phen <- phend[[g]]; phen$label = g; phen[,c('Date', 'label', 'N', 'nff', 'HS', 'SSI', 'GL')]}, simplify=FALSE)), 'Compil_Pheno_treated_archi_sampled.csv',row.names=FALSE)
#
# treated symptom tagged
#
phensym <- lapply(symtagged, pheno_symptom)
#
#check
par(mfrow=c(2,2),mar=c(4,4,1,1))
lapply(names(phendbf), function(g) {
  p <- phendbf[[g]]
  plot(c(0,2500),c(0,14),type='n')
  lapply(split(p,p$N), function(x) points(x$TT,x$HS,col=x$nff,pch=16))
  lapply(split(p,p$N), function(x) points(x$TT,x$SSI,col=x$nff,pch=16,cex=0.7))
  lapply(split(p,p$N), function(x) points(x$TT,x$GL,col=x$nff,pch=16))
  if (g %in% names(phend)){
    phen <- phend[[g]]
    coul <- ifelse(is.na(phen$nff),8,nff)
    symb <- ifelse(is.na(phen$nff),16,1)
    points(phen$TT, phen$HS,pch=symb,col=coul)
    points(phen$TT, phen$SSI, pch=symb, col=coul,cex=0.7)
    points(phen$TT, phen$GL, pch=symb, col=coul)
  }
  if (g %in% names(phensym)){
    phen <- phensym[[g]]
    points(phen$TT, phen$HS, col=phen$nff, pch=6)
    points(phen$TT, phen$SSI, col=phen$nff, pch=6, cex=0.7)
    points(phen$TT, phen$GL, col=phen$nff, pch=6)
    points(phen$TT, phen$GLap, col=phen$nff, pch=21)
  }
})
#
# Export
#
write.csv(do.call('rbind', sapply(names(phensym), function(g) {phen <- phensym[[g]]; phen$label = g; phen[,c('Date', 'label', 'Rep', 'N', 'Axis', 'nff', 'HS', 'SSI', 'GL', 'SSIap','GLap')]}, simplify=FALSE)), 'Compil_Pheno_treated_symptom_tagged.csv',row.names=FALSE)
