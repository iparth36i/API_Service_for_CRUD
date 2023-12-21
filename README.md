# API ervice for CRUD

## API Endpoints

### Add Box

- **Endpoint:** `/api/add/`
- **Method:** `POST`
- **Description:** Adds a new box with given dimensions.
- **Permissions:** User must be logged in and should be a staff member.

### Update Box

- **Endpoint:** `/api/update/<int:pk>/`
- **Method:** `PUT`
- **Description:** Updates dimensions of a box with a given ID.
- **Permissions:** Any staff user can update any box, excluding creator or creation date.

### List All Boxes

- **Endpoint:** `/api/list/`
- **Method:** `GET`
- **Description:** Lists all boxes with optional filters.
- **Permissions:** Any user can see boxes in the store.

### List My Boxes

- **Endpoint:** `/api/my-boxes/`
- **Method:** `GET`
- **Description:** Lists boxes created by the currently logged-in user with optional filters.
- **Permissions:** Only staff users can see their created boxes.

### Delete Box

- **Endpoint:** `/api/delete/<int:pk>/`
- **Method:** `DELETE`
- **Description:** Deletes a box with a given ID.
- **Permissions:** Only the creator of the box can delete it.


## Sample Credentials

To test the API endpoints, you can use the following sample credentials for super user:
1. **Installation:**
- **Username:** `tushar`
- **Password:** `1234`
  
2. **Installation:**
- **Username:** `ricky`
- **Password:** `1234`
  
3. **Installation:**
- **Username:** `minakshi`
- **Password:** `1234`

Please note that these are used to add Boxes as there ther are superuser.
You van also login to admin pannel through this.

- **Endpoint:** `/admin`
