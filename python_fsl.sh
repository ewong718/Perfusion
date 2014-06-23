# FSL Configuration
FSLDIR=/usr/local/fsl
PATH=${FSLDIR}/bin:${PATH}
. ${FSLDIR}/etc/fslconf/fsl.sh
export FSLDIR PATH

inputfile=$1
basename="${inputfile%.nii*}_processed_"
startvol=$2
endvol=$3

fslmaths "${inputfile}" -kernel gauss 0.2 -fmean "${basename}_smooth"
fslroi "${basename}_smooth" "${basename}_PRE" 0 -1 0 -1 0 -1 0 `expr $startvol - 1`
fslroi "${basename}_smooth" "${basename}_DURING" 0 -1 0 -1 0 -1 `expr $startvol - 1` `expr $endvol - $startvol + 1`
fslroi "${basename}_smooth" "${basename}_POST" 0 -1 0 -1 0 -1 `expr $endvol` -1
fslmaths "${basename}_PRE" -Tmean "${basename}_PRE"
fslmaths "${basename}_DURING" -Tmean "${basename}_DURING"
fslmaths "${basename}_POST" -Tmean "${basename}_POST"
fslmaths "${basename}_PRE" -div "${basename}_DURING" "${basename}_B_div_A"