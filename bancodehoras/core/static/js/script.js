function chart() {
    var ctx = document.getElementById('general-vision').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Colaborador 01', 'Colaborador 02', 'Colaborador 03', 'Colaborador 04', 'Colaborador 05'],
            datasets: [{
                label: 'Total de horas dos colaboradores do meu setor',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function mostraGraficoDoColaborador() {
    var ctx = document.getElementById('chart-colaborador-extras-cadastrados');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["janeiro", "fevereiro", "Março", "Abriu", "Maio", "Junho"],
            datasets: [{
                label: "Total de banco de horas por mês",
                data: [65, 59, 80, 81, 56, 55],
                backgroundColor: "rgba(33,150,243,0.0)",
                borderColor: "rgba(33,150,243,1)",
                borderCapsStyle: "butt",
                paintBorderColor: "rgba(33,150,243,1)",
                pointBorderColor: "rgba(171,71,188,1)",
                pointBackgroundColor: "#fff"
            },
            {
                label: "Total de baixas por mês",
                data: [2, 3, 1, 2, 5, 2],
                backgroundColor: "rgba(255, 99, 132, 0.0)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderCapsStyle: "butt",
                paintBorderColor: "rgba(255, 99, 132, 1)",
                pointBorderColor: "rgba(171,71,188,1)",
                pointBackgroundColor: "#fff"
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'banco de horas / Mês'
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Month'
                    }
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Value'
                    }
                }]
            }
        
        }
    })
    
}

function iniciaChart() {
    chart();
    mostraGraficoDoColaborador();
}

addEventListener('load', iniciaChart);