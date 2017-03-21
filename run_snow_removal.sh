# Set up stuff
WORK=`pwd`
rm -f averages.snr
touch averages.snr
TEQC=${WORK}/teqc
CRX2RNX=${WORK}/CRX2RNX
mkdir plot_files 2>/dev/null
cd plot_files

years=("2008" "2016")
days=("001" "365")
station="min0"
echo "# ${station} ${years[@]} ${days[@]}" >> ${WORK}/averages.snr
for yr in  `seq ${years[0]} ${years[1]}`; do
    for d in `seq ${days[0]} ${days[1]}`; do
        d3=`printf "%0.3d" ${d}`
        mkdir "${yr}_${d3}" 2>/dev/null
        cd ${yr}_${d3}
        cp ${WORK}/DATA/*${d3}0.${yr: 2:4}d.Z .
        cp ${WORK}/DATA/*${d3}0.${yr: 2:4}n.Z .
        \gzip -df -f  *.Z
        ${CRX2RNX} *d
        ${TEQC} +qcq +plot *o > /dev/null 2>&1
        rm -f *.m12
        rm -f *.m21
        rm -f *.i12
        rm -f *.d12
        data=`python3 ${WORK}/snow_removal.py "min0${d3}0"`
        if [ $? == 0 ]; then
            echo ${yr} ${d3} ${data} >> ${WORK}/averages.snr
        fi
        cd ..
    done
done

rm -rf plot_files


