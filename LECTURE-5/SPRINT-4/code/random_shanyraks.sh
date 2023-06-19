#!/bin/bash

# Array of 75 addresses
addresses=(
    "17 Kabanbay Batyr Street"
    "24 Tole Bi Street"
    "9 Abay Avenue"
    "37 Dostyk Avenue"
    "63 Zheltoksan Street"
    "18 Kirov Street"
    "52 Gogol Street"
    "29 Samal-2 Microdistrict"
    "6 Baiseitova Street"
    "43 Pushkin Street"
    "21 Kurmangazy Street"
    "13 Zhibek Zholy Avenue"
    "32 Seyfullin Street"
    "8 Bogenbay Batyr Street"
    "51 Furmanov Street"
    "27 Al-Farabi Avenue"
    "45 Gagarin Avenue"
    "14 Satpayev Street"
    "38 Abylay Khan Avenue"
    "10 Makataev Street"
    "54 Auezov Street"
    "19 Rozybakiev Street"
    "35 Suyunbai Avenue"
    "7 Kunaev Street"
    "49 Kabanbay Batyr Street"
    "22 Tole Bi Street"
    "12 Abay Avenue"
    "41 Dostyk Avenue"
    "67 Zheltoksan Street"
    "26 Kirov Street"
    "59 Gogol Street"
    "34 Samal-2 Microdistrict"
    "3 Baiseitova Street"
    "47 Pushkin Street"
    "15 Kurmangazy Street"
    "8 Zhibek Zholy Avenue"
    "30 Seyfullin Street"
    "4 Bogenbay Batyr Street"
    "49 Furmanov Street"
    "25 Al-Farabi Avenue"
    "31 Kabanbay Batyr Street"
    "16 Tole Bi Street"
    "11 Abay Avenue"
    "39 Dostyk Avenue"
    "65 Zheltoksan Street"
    "20 Kirov Street"
    "53 Gogol Street"
    "28 Samal-2 Microdistrict"
    "5 Baiseitova Street"
    "42 Pushkin Street"
    "20 Kurmangazy Street"
    "14 Zhibek Zholy Avenue"
    "31 Seyfullin Street"
    "7 Bogenbay Batyr Street"
    "50 Furmanov Street"
    "26 Al-Farabi Avenue"
    "44 Gagarin Avenue"
    "13 Satpayev Street"
    "37 Abylay Khan Avenue"
    "11 Makataev Street"
    "57 Auezov Street"
    "16 Rozybakiev Street"
    "32 Suyunbai Avenue"
    "9 Kunaev Street"
    "53 Kabanbay Batyr Street"
    "18 Tole Bi Street"
    "7 Abay Avenue"
    "35 Dostyk Avenue"
    "61 Zheltoksan Street"
    "23 Kirov Street"
    "48 Gogol Street"
    "27 Samal-2 Microdistrict"
    "4 Baiseitova Street"
    "40 Pushkin Street"
    "19 Kurmangazy Street"
    "11 Zhibek Zholy Avenue"
    "28 Seyfullin Street"
    "2 Bogenbay Batyr Street"
)

# Loop for 75 requests
for ((i=0; i<75; i++))
do
    # Generate random values
    random_type=("Apartment" "Cave" "Lecture Room at Satpayev University")
    random_price=$((RANDOM % 100001))
    random_address=${addresses[$i]}
    random_rooms_count=$((RANDOM % 322 + 1))

    # Send HTTP request
    curl -X 'POST' \
        'http://localhost:8000/shanyraks/' \
        -H 'accept: application/json' \
        -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NDkwOWMyODJjNTU3YjgzNjBlYmY4NDciLCJleHAiOjE2ODg0NTg3NzF9.eUT96ShgaunydVEhsMAdNfJ6oYtwS6DZSXia7dKeDNU' \
        -H 'Content-Type: application/json' \
        -d '{
        "type": "'"$random_type"'",
        "price": '"$random_price"',
        "address": "'"$random_address"'",
        "rooms_count": '"$random_rooms_count"'
    }'

    echo "Request $((i+1)) sent with random values:"
    echo "Type: $random_type"
    echo "Price: $random_price"
    echo "Address: $random_address"
    echo "Rooms Count: $random_rooms_count"
    echo ""
done
