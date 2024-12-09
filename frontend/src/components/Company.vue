<!-- templates/companies.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Companies</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>
    <div class="container mt-5">
        <h1>Companies</h1>
        <button class="btn btn-primary mb-3" data-toggle="modal" data-target="#addCompanyModal">Add Company</button>
        <ul id="company-list" class="list-group">
            <!-- Companies will be listed here -->
        </ul>
    </div>

    <!-- Modal for adding a new company -->
    <div class="modal fade" id="addCompanyModal" tabindex="-1" role="dialog" aria-labelledby="addCompanyModalLabel" aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="addCompanyModalLabel">Add New Company</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                <div class="modal-body">
                    <form id="add-company-form">
                        <div class="form-group">
                            <label for="name">Company Name</label>
                            <input type="text" class="form-control" id="name" required>
                        </div>
                        <div class="form-group">
                            <label for="warehouse">Warehouse</label>
                            <input type="text" class="form-control" id="warehouse" required>
                        </div>
                        <div class="form-group">
                            <label for="inn">INN</label>
                            <input type="text" class="form-control" id="inn" required>
                        </div>
                        <button type="submit" class="btn btn-primary">Add Company</button>
                    </form>
                </div>
            </div>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.bundle.min.js"></script>
    <script>
        // Fetch and display companies
        function fetchCompanies() {
            fetch('/companies/')
                .then(response => response.json())
                .then(data => {
                    const companyList = document.getElementById('company-list');
                    companyList.innerHTML = '';
                    data.forEach(company => {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';
                        li.textContent = company.name;
                        companyList.appendChild(li);
                    });
                });
        }

        // Add company form submit
        document.getElementById('add-company-form').addEventListener('submit', function(event) {
            event.preventDefault();
            const name = document.getElementById('name').value;
            const warehouse = document.getElementById('warehouse').value;
            const inn = document.getElementById('inn').value;

            fetch('/companies/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name, warehouse, inn }),
            })
            .then(response => response.json())
            .then(data => {
                $('#addCompanyModal').modal('hide');
                fetchCompanies();
            });
        });

        // Initial fetch
        fetchCompanies();
    </script>
</body>
</html>
