library(RMySQL)
library(pracma)
con <- dbConnect(RMySQL::MySQL(), dbname = 'optfinal', username = 'root', password = 'root')
dcs <- dbReadTable(con,"ww_dcs")
stores <- dbReadTable(con, "ww_stores")

dcs.location <- as.vector(dcs[6:7])
stores.location <- as.vector(stores[2:3])


ww_mileage <- matrix(nrow = nrow(dcs.location)*nrow(stores.location), ncol = 3, byrow = T)
colnames(ww_mileage) <- c("dc_id", "store_id", "mileage")
#head(ww_mileage)
nrow(ww_mileage)

n <- 0
for (i in 1:nrow(dcs.location)){
  for (j in 1:nrow(stores.location)){
    n=n+1
    ww_mileage[n,1] <- dcs$dc_id[i]
    ww_mileage[n,2] <- stores$store_id[j]
    ww_mileage[n,3] <- haversine(c(dcs.location$lat[i],dcs.location$lon[i]),c(stores.location$lat[j],stores.location$lon[j]))
  } 
}

head(ww_mileage)

for (i in 1:nrow(ww_mileage)){
  dbSendQuery(con, sprintf("insert into ww_mileage (dc_id, store_id, mileage) values ('%s', '%s','%s')", ww_mileage[i,1], ww_mileage[i,2],ww_mileage[i,3])) #send the data to MySQL
}
dbDisconnect(con) #disconnect to stop memory leaks