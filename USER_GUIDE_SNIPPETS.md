## User Guide Snippets (Conceptual)

### Logging In
1.  Access the application URL.
2.  If not logged in, a login prompt or login button will appear.
3.  Enter your username and password.
4.  Upon successful login, the dashboard or main view will be displayed.

### Navigating the Application
*   Use the sidebar navigation links (Dashboard, TA Records, Experts, Templates) to switch between different sections.
*   The main content area will update dynamically.

### TAF Records
*   **Viewing:** Click 'TA Records' (or 'All', 'Ongoing', 'Closed') to see a list of records. Use pagination if many records exist.
*   **Filtering:** Use the filter panel in the sidebar to narrow down records by Country, Expert, Theme, etc. Click 'Apply Filters'.
*   **Searching:** (If a search bar is present in the TAF Records view) Enter keywords to search.
*   **Viewing Details:** Click on a record's ID or a 'View' icon to see its full details and attachments.
*   **Downloading Attachments:** On the details page, find the 'Associated Files' section. Click on a file name to download it.

### TAF Records (Admin Only)
*   **Adding a New Record:**
    1.  Click 'Add New Record' (either in sidebar or on TA Records page).
    2.  Fill out the form fields. Required fields are marked.
    3.  For file attachments, navigate through the file category tabs, click 'Add File to [Category]', and select your file(s).
    4.  Click 'Save Record'.
*   **Editing a Record:**
    1.  In the TAF Records list, click the 'Edit' (pencil) icon for the desired record.
    2.  Modify the form fields and/or manage attachments.
    3.  Click 'Save Record'.
*   **Deleting a Record:**
    1.  In the TAF Records list, click the 'Delete' (trash) icon.
    2.  Confirm the deletion in the modal.
*   **Deleting an Attachment (from View Record page):**
    1.  Navigate to the record's detail page.
    2.  In the 'Associated Files' section, find the file and click its 'Delete' (trash) icon.
    3.  Confirm deletion.

### Templates
*   **Viewing/Downloading (All Users):** Click 'Templates'. Templates are listed by category. Click 'View/Download' for a template.
*   **Uploading (Admin Only):**
    1.  On the Templates page, click 'Upload New Template'.
    2.  Provide a Template Name, select a Category, and choose the file.
    3.  Click 'Upload Template'.
*   **Deleting (Admin Only):**
    1.  On the Templates page, click the 'Delete' (trash) icon for the desired template.
    2.  Confirm deletion.

### Experts
*   **Viewing (All Users):** Click 'Experts' to see a list of available experts and their details.

### Dashboard
*   **Viewing (All Users):** Click 'Dashboard' to see overview statistics and charts related to TAF records.

### Backups (Admin Only - via API or external tool)
*   Admins can use API tools (like Postman, curl) or custom scripts to interact with the backup API endpoints (see README API section) to trigger, list, and download backups. A UI for this is not part of the current frontend.
