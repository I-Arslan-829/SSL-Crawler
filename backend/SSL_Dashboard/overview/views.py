from django.http import JsonResponse
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from django.conf import settings




client = MongoClient(
    host=settings.MONGODB_HOST,
    port=settings.MONGODB_PORT,
)
db = client[settings.MONGODB_DATABASE]
certs = db["certificates"]

def overview_data(request):
    now = datetime.now(timezone.utc)
    now_iso = now.isoformat().replace('+00:00', 'Z')
    soon_iso = (now + timedelta(days=30)).isoformat().replace('+00:00', 'Z')

    # 1. SUMMARY FIELDS
    total_certificates = certs.count_documents({})
    active_certificates = certs.count_documents({
        "parsed.validity.end": { "$gte": now_iso }
    })
    expired_certificates = certs.count_documents({
        "parsed.validity.end": { "$lt": now_iso }
    })
    expiring_soon_certificates = certs.count_documents({
        "parsed.validity.end": {
            "$gte": now_iso,
            "$lte": soon_iso
        }
    })

    # Unique domains and issuers
    unique_domains = certs.distinct("parsed.subject.common_name.0")
    unique_issuers = certs.distinct("parsed.issuer.organization.0")

    # Validation levels
    pipeline = [
        {"$group": {"_id": "$parsed.validation_level", "count": { "$sum": 1 }}}
    ]
    validation_levels = list(certs.aggregate(pipeline))
    validation_levels_dict = {
        item["_id"]: item["count"] for item in validation_levels if item["_id"] is not None
    }


    # Pagination parameters
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 50))
    skip = (page - 1) * page_size

    # Total for all matching documents (for frontend pagination UI)
    total_rows = certs.count_documents({})

    # Cursor fetch with skip/limit (MUST have index for fast skip, or use cursor-based "after" for biggest DBs)
    cursor = certs.find({}, {
        "domain": 1,
        "parsed.subject.common_name": 1,
        "parsed.extensions.subject_alt_name.dns_names": 1,
        "parsed.issuer.organization": 1,
        "parsed.issuer.common_name": 1,
        "parsed.issuer.country": 1,
        "parsed.validation_level": 1,
        "parsed.signature_algorithm.name": 1,
        "parsed.subject_key_info.key_algorithm.name": 1,
        "parsed.validity.start": 1,
        "parsed.validity.end": 1,
        "parsed.fingerprint_sha256": 1,
        "parsed.serial_number": 1,
    }).sort("parsed.validity.end", -1).skip(skip).limit(page_size)

    table_rows = []
    now = datetime.now(timezone.utc)
    for doc in cursor:
        # Same field extraction and datetime fix as previous code:
        # ...
        # (see previous answer for table_rows logic)
        end = doc.get("parsed", {}).get("validity", {}).get("end")
        end_dt = None
        if end:
            try:
                end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
            except Exception:
                pass
        days_remaining = (end_dt - now).days if end_dt else None

        table_rows.append({
            "domain": doc.get("parsed", {}).get("subject", {}).get("common_name", [""])[0],
            "san": doc.get("parsed", {}).get("extensions", {}).get("subject_alt_name", {}).get("dns_names", []),
            "issuer_org": doc.get("parsed", {}).get("issuer", {}).get("organization", [""])[0],
            "issuer_cn": doc.get("parsed", {}).get("issuer", {}).get("common_name", [""])[0],
            "validation_level": doc.get("parsed", {}).get("validation_level", ""),
            "signature_algorithm": doc.get("parsed", {}).get("signature_algorithm", {}).get("name", ""),
            "public_key_algorithm": doc.get("parsed", {}).get("subject_key_info", {}).get("key_algorithm", {}).get("name", ""),
            "start_date": doc.get("parsed", {}).get("validity", {}).get("start"),
            "expiration_date": end,
            "days_remaining": days_remaining,
            "expired": (days_remaining is not None and days_remaining < 0),
            "issuer_country": doc.get("parsed", {}).get("issuer", {}).get("country", [""])[0],
            "fingerprint_sha256": doc.get("parsed", {}).get("fingerprint_sha256", ""),
            "serial_number": doc.get("parsed", {}).get("serial_number", ""),
        })

    data = {
        "summary": {
            "total_certificates": total_certificates,
            "active_certificates": active_certificates,
            "expired_certificates": expired_certificates,
            "expiring_soon": expiring_soon_certificates,
            "unique_domains_count": len(unique_domains),
            "unique_issuers_count": len(unique_issuers),
            "validation_levels": validation_levels_dict,
        },
        "table": table_rows,
        "total_rows": total_rows,
        "page": page,
        "page_size": page_size,
    }
    return JsonResponse(data, safe=False)































# from django.http import JsonResponse
# from pymongo import MongoClient
# from datetime import datetime, timedelta, timezone
# from django.conf import settings

# client = MongoClient(
#     host=settings.MONGODB_HOST,
#     port=settings.MONGODB_PORT,
# )
# db = client[settings.MONGODB_DATABASE]
# certs = db["certificates"]

# def overview_data(request):
#     now = datetime.now(timezone.utc)
#     now_iso = now.isoformat().replace('+00:00', 'Z')
#     soon_iso = (now + timedelta(days=30)).isoformat().replace('+00:00', 'Z')

#     # 1. SUMMARY FIELDS
#     total_certificates = certs.count_documents({})
#     active_certificates = certs.count_documents({
#         "parsed.validity.end": { "$gte": now_iso }
#     })
#     expired_certificates = certs.count_documents({
#         "parsed.validity.end": { "$lt": now_iso }
#     })
#     expiring_soon_certificates = certs.count_documents({
#         "parsed.validity.end": {
#             "$gte": now_iso,
#             "$lte": soon_iso
#         }
#     })

#     # Unique domains and issuers
#     unique_domains = certs.distinct("parsed.subject.common_name.0")
#     unique_issuers = certs.distinct("parsed.issuer.organization.0")

#     # Validation levels
#     pipeline = [
#         {"$group": {"_id": "$parsed.validation_level", "count": { "$sum": 1 }}}
#     ]
#     validation_levels = list(certs.aggregate(pipeline))
#     validation_levels_dict = {
#         item["_id"]: item["count"] for item in validation_levels if item["_id"] is not None
#     }

#     # 2. TABLE DATA - fetch all certificates (be careful for huge collections!)
#     table_rows = []
#     cursor = certs.find({}, {
#         "domain": 1,
#         "parsed.subject.common_name": 1,
#         "parsed.extensions.subject_alt_name.dns_names": 1,
#         "parsed.issuer.organization": 1,
#         "parsed.issuer.common_name": 1,
#         "parsed.issuer.country": 1,
#         "parsed.validation_level": 1,
#         "parsed.signature_algorithm.name": 1,
#         "parsed.subject_key_info.key_algorithm.name": 1,
#         "parsed.validity.start": 1,
#         "parsed.validity.end": 1,
#         "parsed.fingerprint_sha256": 1,
#         "parsed.serial_number": 1,
#     }).sort("parsed.validity.end", -1)

#     for doc in cursor:
#         start = doc.get("parsed", {}).get("validity", {}).get("start")
#         end = doc.get("parsed", {}).get("validity", {}).get("end")
#         end_dt = None
#         if end:
#             try:
#                 end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
#             except Exception:
#                 pass
#         days_remaining = (end_dt - now).days if end_dt else None

#         table_rows.append({
#             "domain": doc.get("parsed", {}).get("subject", {}).get("common_name", [""])[0],
#             "san": doc.get("parsed", {}).get("extensions", {}).get("subject_alt_name", {}).get("dns_names", []),
#             "issuer_org": doc.get("parsed", {}).get("issuer", {}).get("organization", [""])[0],
#             "issuer_cn": doc.get("parsed", {}).get("issuer", {}).get("common_name", [""])[0],
#             "validation_level": doc.get("parsed", {}).get("validation_level", ""),
#             "signature_algorithm": doc.get("parsed", {}).get("signature_algorithm", {}).get("name", ""),
#             "public_key_algorithm": doc.get("parsed", {}).get("subject_key_info", {}).get("key_algorithm", {}).get("name", ""),
#             "start_date": start,
#             "expiration_date": end,
#             "days_remaining": days_remaining,
#             "expired": (days_remaining is not None and days_remaining < 0),
#             "issuer_country": doc.get("parsed", {}).get("issuer", {}).get("country", [""])[0],
#             "fingerprint_sha256": doc.get("parsed", {}).get("fingerprint_sha256", ""),
#             "serial_number": doc.get("parsed", {}).get("serial_number", ""),
#         })

#     data = {
#         "summary": {
#             "total_certificates": total_certificates,
#             "active_certificates": active_certificates,
#             "expired_certificates": expired_certificates,
#             "expiring_soon": expiring_soon_certificates,
#             "unique_domains_count": len(unique_domains),
#             "unique_issuers_count": len(unique_issuers),
#             "validation_levels": validation_levels_dict,
#         },
#         "table": table_rows
#     }
#     return JsonResponse(data, safe=False)
