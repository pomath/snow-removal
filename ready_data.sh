# Set up stuff
WORK=`pwd`
mkdir plot_files
cd plot_files
years=("2015" "2016")
days=("001" "365")
for yr in ${years[@]}; do
    for d in `seq ${days[0]} ${days[1]}`; do
        mkdir "${yr}_${d}"
        cp "${WORK}/DATA/*${d}0.${yr: 2:4}?.Z" "${yr}_${d}"
        unzip *.Z
        teqc +qcq +plot *o
        rm -f *.Z
        rm -f *.m12
        rm -f *.m21
        rm -f *.i12
        rm -f *.d12
    done
done

# Run python script on the plot files


# Clean up

