function imgtopdf() {
    for f in * 
    do
        echo "Traitement du futur pdf : $f"
        count=`ls "$f"/*.jpg 2>/dev/null | wc -l`
        if [ "$count" -gt 1 ] 
        then
            ext="jpg"
        else
            ext="png"
        fi
        convert "$f/*.$ext" -resize 70% -set units PixelsPerInch "$f".pdf
    done
}

imgtopdf myScan.pdf