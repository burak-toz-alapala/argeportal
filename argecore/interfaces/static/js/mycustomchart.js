
    var chartNameList = ['FillPressures'];
    var colorList = ["#ff5733", "#f39c12", "#9b59b6", "#24e58f", "#00d2ff", "#0077b6", "#182c50"];

    // Kullanılmış renkleri takip etmek için bir Set
    var usedColors = new Set();

  
  // Kullanılmayan rastgele bir renk seçen fonksiyon
  function getRandomColor() {
    if (usedColors.size >= colorList.length) {
        usedColors.clear(); // Tüm renkler kullanıldıysa sıfırla
    }

    let availableColors = colorList.filter(color => !usedColors.has(color));
    let randomColor = availableColors[Math.floor(Math.random() * availableColors.length)];

    usedColors.add(randomColor);
    return randomColor;
}

// Generic AJAX function to fetch and render chart data
function fetchChartData(url, chartKey, chartName, root_url) {

    document.getElementById("loading" + chartName).style.display = "grid"; // Yüklenme çubuğunu göster
    document.getElementById("lineChart" + chartName).style.display = "none"; // Grafiği gizle



    $.ajax({
        url: root_url + url,
        type: 'GET',
        success: function (response) {
            // const data = JSON.parse(response);
            const data = response;
            const option = createChartOption(data.dates, data.series, chartTitles[chartKey]);
            chartInstances[chartKey].setOption(option);
            document.getElementById("loading" + chartName).style.display = "none"; // Yüklenme çubuğunu gizle
            document.getElementById("lineChart" + chartName).style.display = "block"; // Grafiği göster
            updateAllChartsForMediaQuery(option, chartKey);

        },
        error: function () {
            alert('Veri yüklenemedi.');
        }
    });
}

// Generate ECharts option object
function createChartOption(dates, seriesData, titleText) {
    const mediaQuery = window.matchMedia('(min-width: 768px) and (max-width: 991.98px)');
    const titleTop = mediaQuery.matches ? '10%' : '5%'; // Dinamik top değeri
    const legendTop = mediaQuery.matches ? '15%' : '1%'; // Dinamik legend top değeri

    return {
        title: {
            text: titleText,
            top: '10%',
            left: 'center',
            // padding: [10, 20, 20, 20],
            textStyle: { fontSize: 18 }
        },
        grid: {
            top: '20%', // Grafik ile başlık arasındaki boşluğu ayarlamak için grafiğin üst kısmındaki boşluğu artırıyoruz
            left: '5%',
            right: '5%',
            bottom: '5%',
            containLabel: true
        },
        toolbox: {
            right: 10,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                restore: {},
                saveAsImage: {}
            }
        },
        dataZoom: [

            {
                type: 'inside'
            }
        ],
        tooltip: { trigger: 'axis' },
        legend: {
            top: '0%',
            data: seriesData.map(serie => serie.name),
            type: 'scroll', // Kaydırılabilir tür
            orient: 'horizontal', // Yatay yön
            left: 'center',
            align: 'auto',
            itemWidth: 20, // İkon genişliği
            itemHeight: 14, // İkon yüksekliği
            pageButtonItemGap: 5, // Kaydırma düğmeleri arası boşluk
            pageButtonGap: 5, // Sayfa düğmeleri ile içerik arası boşluk
        },
        xAxis: { type: 'category', data: dates },
        yAxis: { 
            type: 'value', 
            interval: 0.005,
            axisLabel: {
                // margin: 20 // Y eksenindeki yazılar için kenar boşluğu
                formatter: function (value) {
                    // value: Eksenin sayısal değeri
                    return value.toFixed(3); // Sayıyı virgülden sonra 4 basamaklı gösterir
                }
            }
         },
        series: seriesData.map(serie => ({
            name: serie.name,
            data: serie.values,
            type: 'line',
            color: getRandomColor() // Her seriye farklı bir renk atanıyor
        }))
    };
}

// Grafik medya sorgusunu kontrol eden bir fonksiyon
function updateChartOptions(option, chartKey) {
    const mediaQuery = window.matchMedia('(min-width: 768px) and (max-width: 991.98px)');


    // if (mediaQuery.matches) {
    //     // Orta boyutlu ekranlar için ayarlar
    //     option.title.top = '3%';
    // } else {
    //     // Varsayılan ayarlar
    //     option.title.top = '5%';
    // }

    // chartInstances[chartKey].setOption(option); // Yeni ayarları uygula
}

// Her grafik için medya sorgusu fonksiyonunu çağır
function updateAllChartsForMediaQuery(option, chartKey) {
    updateChartOptions(option, chartKey);
}

// Zaman aralığı seçildiğinde grafiği otomatik yenileyen fonksiyon
function resetDateAllChart() {
    // Iterate over each chart name
    for (let chartName of chartNameList) {
        // Generate the input IDs
        const startDateId = 'startDate' + chartName;
        const endDateId = 'endDate' + chartName;

        // Reset the dates using the IDs
        resetDateById(startDateId);
        resetDateById(endDateId);

    }
}

function resetDateById(inputId) {
    document.getElementById(inputId).value = "";
}

function getDateById(inputId) {
    var dateInput = document.getElementById(inputId).value;

    // Eğer input boşsa, haftanın başlangıç veya bitiş tarihini belirle
    if (dateInput == "") {
        const today = new Date();
        const dayOfWeek = today.getDay(); // 0: Pazar, 1: Pazartesi, ..., 6: Cumartesi

        // Haftanın başlangıcı (Pazartesi)
        if (inputId.includes("start")) {
            var startOfWeek = new Date(today);
            var daysToSubtract = (dayOfWeek === 0) ? 6 : (dayOfWeek - 1); // Eğer Pazar ise 6 gün geri git
            startOfWeek.setDate(today.getDate() - daysToSubtract);
            // Saat ve dakikayı ayarla
            startOfWeek.setUTCHours(0, 0, 0, 0); // 00:00
            dateInput = startOfWeek.toISOString();
        }

        // Haftanın sonu (Pazar)
        else if (inputId.includes("end")) {
            var endOfWeek = new Date(today);
            var daysToAdd = (dayOfWeek === 0) ? 0 : (7 - dayOfWeek); // Eğer Pazar ise 0 gün ekle
            endOfWeek.setDate(today.getDate() + daysToAdd);
            // Saat ve dakikayı ayarla
            endOfWeek.setUTCHours(23, 59, 59, 999); // 23:59
            dateInput = endOfWeek.toISOString();
        }
    }

    // Tarih ve saati ayırmak için `split()` fonksiyonunu kullanın
    const dateParts = dateInput.split('T');

    // Yıl, ay, gün, saat ve dakikayı ayrı değişkenlere atayın
    const year = dateParts[0].split('-')[0];
    const month = dateParts[0].split('-')[1];
    const day = dateParts[0].split('-')[2];
    const hour = dateParts[1].split(':')[0];
    const minute = dateParts[1].split(':')[1];

    // Dizeyi birleştirmek için `concat()` fonksiyonunu kullanın
    const formattedDate = year.concat(month, day, hour, minute);

    return formattedDate;
}



function getChartData(url, chartKey, chartName, root_url) {
    fetchChartData(url, chartKey, chartName, root_url);
}



//     // Tarayıcı boyutlandırıldığında medya sorgusunu kontrol et
// window.addEventListener('resize', fetchAllCharts);
function resizeCharts() {
    Object.values(chartInstances).forEach(chart => chart.resize());
}

window.addEventListener('resize', () => resizeCharts);

