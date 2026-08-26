const {
    ClassicEditor,
    Essentials,
    Bold,
    Italic,
    Font,
    Paragraph
} = CKEDITOR;

const editorConfig = {
    licenseKey: LICENSE_KEY,
            plugins: [ Essentials, Bold, Italic, Font, Paragraph ],
            toolbar: [
                'undo', 'redo', '|', 'bold', 'italic', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor'
            ]
}

ClassicEditor
    .create(document.querySelector( '#body' ), editorConfig)
      .then(editor => {
            // Synchronize data back to the hidden textarea on submit
            editor.model.document.on('change:data', () => {
                document.querySelector('#body').value = editor.getData();
            });
        })
        .catch(error => {
            console.error(error);
        });

ClassicEditor
    .create(document.querySelector( '#comment_text' ), editorConfig)
      .then(editor => {
            // Synchronize data back to the hidden textarea on submit
            editor.model.document.on('change:data', () => {
                document.querySelector('#comment_text').value = editor.getData();
            });
        })
        .catch(error => {
            console.error(error);
        });