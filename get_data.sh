WORK=`pwd`
mkdir DATA
cd DATA
years=("2008" "2016")
days=("001" "365")
station="min0"
for yr in ${years[@]}; do
    for d in `seq ${days[0]} ${days[1]}`; do
        d3=`printf "%0.3d" ${d}`
        wget ftp://data-out.unavco.org/pub/rinex/obs/${yr}/${d3}/${station}*d.Z
        wget ftp://data-out.unavco.org/pub/rinex/nav/${yr}/${d3}/${station}*n.Z
    done
done

