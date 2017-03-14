# Set up stuff
WORK=`pwd`
rm -f averages.snr
touch averages.snr
TEQC=./teqc
CRX2RNX=./CRX2RNX
mkdir plot_files 2>/dev/null
cd plot_files

years=("2016")
days=("001" "365")
station="min0"
echo "# ${station} ${years[@]} ${days[@]}" >> ${WORK}/averages.snr
for yr in ${years[@]}; do
    for d in `seq ${days[0]} ${days[1]}`; do
        prog=$(python -c "print('{:4.4}'.format(${d}/${days[1]}*100))")
        echo -ne "      ${prog}\r"
        d3=`printf "%0.3d" ${d}`
        mkdir "${yr}_${d3}" 2>/dev/null
        cd ${yr}_${d3}
        cp ${WORK}/DATA/*${d3}0.${yr: 2:4}o.Z .
        cp ${WORK}/DATA/*${d3}0.${yr: 2:4}n.Z .
        gzip -df *.Z
        ${TEQC} +qcq +plot *o > /dev/null 2>&1
        rm -f *.m12
        rm -f *.m21
        rm -f *.i12
        rm -f *.d12
        data=`python ${WORK}/snow_removal.py "min0${d3}0"`
        if [ $? == 0 ]; then
            echo ${yr} ${d3} ${data} >> ${WORK}/averages.snr
        fi
        cd ..
    done
done


