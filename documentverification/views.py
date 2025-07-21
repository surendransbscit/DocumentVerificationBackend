from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import UploadedDocument, ExtractedData
from .serializers import UploadedDocumentSerializer, ExtractedDataSerializer
from .ocr_utils import extract_text_fields
from .llm_utils import validate_passport_llm
from django.http import FileResponse, Http404
from django.conf import settings
import os



class DocumentUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES['file']
        print("uploaded_file:", uploaded_file)

        doc = UploadedDocument.objects.create(
            file=uploaded_file,
            file_type=uploaded_file.content_type,
            ip_address=request.META.get('REMOTE_ADDR'),
            device_info=request.META.get('HTTP_USER_AGENT', ''),
        )
        print("Document created:", doc)


        data = extract_text_fields(doc.file.path)
        print("Extracted data:", data)

        name = data.get("name")
        dob = data.get("dob")
        doc_number = data.get("doc_number")
        expiry_date = data.get("expiry_date")


        verdict = ""
        if name and dob and doc_number and expiry_date:
            verdict = validate_passport_llm(data)
            doc.status = "Verified"
        elif not name and not dob:
            doc.status = "Failed"
            verdict = validate_passport_llm(data) 
        elif not doc_number or not expiry_date:
            doc.status = "Pending"
            verdict = validate_passport_llm(data)
            print("LLM verdict:", verdict)
        else:
            doc.status = "Pending"
        doc.save()

        extracted = ExtractedData.objects.create(
            document=doc,
            raw_text=data.get("raw_text", ""),
            name=name,
            dob=dob,
            doc_number=doc_number,
            expiry_date=expiry_date,
            llm_verdict=verdict
        )

        return Response({
            "Message": "Document uploaded and processed successfully.",
            "document": UploadedDocumentSerializer(doc).data,
            "extracted_data": ExtractedDataSerializer(extracted).data
        }, status=status.HTTP_201_CREATED)




class DocumentListView(APIView):
    def get(self, request):
        docs = UploadedDocument.objects.all().order_by('-uploaded_at')
        serializer = UploadedDocumentSerializer(docs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class DocumentDownloadView(APIView):
    def get(self, request, pk):
        try:
            doc = UploadedDocument.objects.get(pk=pk)
            file_path = doc.file.path
            if os.path.exists(file_path):
                print("File path:", file_path)
                return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
            else:
                raise Http404("File not found.")
        except UploadedDocument.DoesNotExist:
            raise Http404("Document not found.")
        
        
class DocumentDeleteView(APIView):
    def delete(self, request, pk):
        try:
            doc = UploadedDocument.objects.get(pk=pk)

            file_path = doc.file.path
            if os.path.exists(file_path):
                os.remove(file_path)
            doc.delete()
            return Response({"message": "Document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        except UploadedDocument.DoesNotExist:
            raise Http404("Document not found.")
        

class getDocumentFullDetailsView(APIView):
    def get(self, request, pk):
        try:
            doc = UploadedDocument.objects.get(pk=pk)
        except UploadedDocument.DoesNotExist:
            raise Http404("Document not found.")

        extracted_data = ExtractedData.objects.filter(document=doc).first() 

        result = {
            "id": doc.id,
            "file": doc.file.url if doc.file else None,
            "uploaded_at": doc.uploaded_at,
            "file_type": doc.file_type,
            "ip_address": doc.ip_address,
            "device_info": doc.device_info,
            "status": doc.status,
            "raw_text": extracted_data.raw_text if extracted_data else None,
            "name": extracted_data.name if extracted_data else None,
            "dob": extracted_data.dob if extracted_data else None,
            "doc_number": extracted_data.doc_number if extracted_data else None,
            "expiry_date": extracted_data.expiry_date if extracted_data else None,
            "llm_verdict": extracted_data.llm_verdict if extracted_data else None,
        }

        return Response(result, status=status.HTTP_200_OK)

