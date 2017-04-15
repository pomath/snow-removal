WORK=`pwd`
mkdir DATA
cd DATA
years=("2013" "2016")
days=("001" "365")
station="uthw"
for yr in `seq ${years[0]} ${years[1]}`; do
    for d in `seq ${days[0]} ${days[1]}`; do
        d3=`printf "%0.3d" ${d}`
        if [ ! -e "${station}${d3}0.${yr: 2:2}d.Z" ]; then
            wget ftp://data-out.unavco.org/pub/rinex/obs/${yr}/${d3}/${station}*d.Z
        fi

        if [ ! -e "${station}${d3}0.${yr: 2:2}n.Z" ]; then
            wget ftp://data-out.unavco.org/pub/rinex/nav/${yr}/${d3}/${station}*n.Z
        fi
    done
done

