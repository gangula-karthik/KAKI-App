
function generatePDF():{
    const element =  document.getElementById("Content");

    html2pdf().form(element).save();
    }


//function generatePDF() \{
//  const contentElement = document.getElementById('Content');
//
//  // Create a new jsPDF instance
//  const doc = new jsPDF();
//
//  // Convert the HTML and CSS to PDF
//  const options = {
//    html2canvas: { scale: 2 },
//    callback: function () {
//      // Save the PDF
//      doc.save('output.pdf');
//    }
//  };
//  doc.html(contentElement, options);
//}

