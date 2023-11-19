document.addEventListener("DOMContentLoaded", () => {
    // Fonction pour charger des données (simulées)
    const loadData = (chartId, data) => {
        const chart = d3.select(chartId);
        chart.selectAll("*").remove(); // Effacez le contenu précédent

        // Exemple de création de graphique à barres
        const margin = { top: 20, right: 30, bottom: 40, left: 40 };
        const width = 400 - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;

        const svg = chart
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleBand()
            .domain(data.map(d => d.label))
            .range([0, width])
            .padding(0.1);

        const y = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.value)])
            .nice()
            .range([height, 0]);

        svg.selectAll(".bar")
            .data(data)
            .enter()
            .append("rect")
            .attr("class", "bar")
            .attr("x", d => x(d.label))
            .attr("y", d => y(d.value))
            .attr("width", x.bandwidth())
            .attr("height", d => height - y(d.value));

        svg.append("g")
            .attr("class", "x-axis")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(x));

        svg.append("g")
            .attr("class", "y-axis")
            .call(d3.axisLeft(y));
    };

    // Gestionnaire de clic pour charger des données utilisateur (exemple de données fictives)
    document.getElementById("load-user-data").addEventListener("click", () => {
        const userData = [
            { label: "N", value: 10 },
            { label: "P", value: 15 },
            { label: "K", value: 8 },
            { label: "pH", value: 12 },
        ];
        loadData("#user-chart", userData);
    });

    // Gestionnaire de clic pour charger des données administrateur (exemple de données fictives)
    document.getElementById("load-admin-data").addEventListener("click", () => {
        const adminData = [
            { label: "N", value: 30 },
            { label: "P", value: 25 },
            { label: "K", value: 20 },
            { label: "pH", value: 15 },
        ];
        loadData("#admin-chart", adminData);
    });

    // Gestionnaire de clic pour charger la matrice de corrélation
    document.getElementById("load-correlation-matrix").addEventListener("click", () => {
        // Exemple de création d'un graphique circulaire (camembert)
        const createPieChart = (data) => {
    // Utilisez les données pour créer le graphique circulaire
    // Assurez-vous d'adapter le code pour vos données spécifiques
    };

    // Utilisation :
        const userData = [
            { label: "N", value: 10 },
            { label: "P", value: 15 },
            { label: "K", value: 8 },
            { label: "pH", value: 12 },
        ];
        createPieChart(userData);
        // Chargez et créez la matrice de corrélation ici
        // Assurez-vous d'adapter le code pour utiliser vos propres données
    });

    // Gestionnaire de clic pour charger d'autres types de graphiques
    document.getElementById("load-other-graph").addEventListener("click", () => {
        // Chargez et créez d'autres types de graphiques ici
        // Assurez-vous d'adapter le code pour utiliser vos propres données
		// Exemple de création d'une matrice de corrélation
        const createCorrelationMatrix = (data) => {
        // Utilisez les données pour créer la matrice de corrélation
        // Assurez-vous d'adapter le code pour vos données spécifiques
    };

      // Utilisation :
         const correlationData = [
             [1.0, 0.8, 0.6],
             [0.8, 1.0, 0.7],
             [0.6, 0.7, 1.0],
        ];
        createCorrelationMatrix(correlationData);

    });
});

    const fetchData = async (source, chartId) => {
        try {
            const response = await fetch(source);
            if (!response.ok) {
                throw new Error("Erreur lors du chargement des données.");
            }
            const data = await response.json();
            loadData(chartId, data);
        } catch (error) {
            console.error(error);
        }
    };

    document.getElementById("load-user-data").addEventListener("click", () => {
        const userDataUrl = "user-data.json"; // URL pour les données utilisateur
        fetchData(userDataUrl, "#user-chart");
    });

    document.getElementById("load-admin-data").addEventListener("click", () => {
        const adminDataUrl = "admin-data.json"; // URL pour les données administrateur
        fetchData(adminDataUrl, "#admin-chart");
    });
});
