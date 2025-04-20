import Midtrans from "midtrans-client"

let snap = new Midtrans.Snao({
    isProduction: False;
    serverKey: process.env.SECRET, 
    clientKe
})
export async functin POST(request){
    const {name, price, quantity, total_price, category, item_id} = await request.json()

    let parameter = {
        item_details: {
            name : name , 
            price : price; 
            quantity : quantity;
            total_price : total_price;
        }
        transaction_details :{
        'transaction_id': transaction_id,
        gross_amount = price * quantity
    }

    const token = await snap.createTransactionToken(parameter)
    console.log(token)
    nextResponse.json({ token })
    
            
        }
    }
}

import midtransclient
# Create Snap API instance
snap = midtransclient.Snap(
    # Set to true if you want Production Environment (accept real transaction).
    is_production=False,
    server_key='YOUR_SERVER_KEY'
)
# Build API parameter
param = {
    "transaction_details": {
        "order_id": "test-transaction-123",
        "gross_amount": 200000
    }, "credit_card":{
        "secure" : True
    }, "customer_details":{
        "first_name": "budi",
        "last_name": "pratama",
        "email": "budi.pra@example.com",
        "phone": "08111222333"
    }
}

transaction = snap.create_transaction(param)

transaction_token = transaction['token']

{
  "transaction_details": {
    "order_id": "ORDER-101",
    "gross_amount": 10000
  },
  "item_details": [{
    "id": "ITEM1",
    "price": 10000,
    "quantity": 1,
    "name": "Midtrans Bear",
    "brand": "Midtrans",
    "category": "Toys",
    "merchant_name": "Midtrans",
    "url": "http://toko/toko1?item=abc"
  }],
  "customer_details": {
    "first_name": "TEST",
    "last_name": "MIDTRANSER",
    "email": "test@midtrans.com",
    "phone": "+628123456",
    "billing_address": {
      "first_name": "TEST",
      "last_name": "MIDTRANSER",
      "email": "test@midtrans.com",
      "phone": "081 2233 44-55",
      "address": "Sudirman",
      "city": "Jakarta",
      "postal_code": "12190",
      "country_code": "IDN"
    },
    "shipping_address": {
      "first_name": "TEST",
      "last_name": "MIDTRANSER",
      "email": "test@midtrans.com",
      "phone": "0 8128-75 7-9338",
      "address": "Sudirman",
      "city": "Jakarta",
      "postal_code": "12190",
      "country_code": "IDN"
    }
  },
  "enabled_payments": ["credit_card", "cimb_clicks",
    "bca_klikbca", "bca_klikpay", "bri_epay", "echannel", "permata_va",
    "bca_va", "bni_va", "bri_va","cimb_va", "other_va", "gopay", "indomaret",
    "danamon_online", "akulaku", "shopeepay", "kredivo", "uob_ezpay","other_qris" ],
  
  "credit_card": {
    "secure": true,
    "channel": "migs",
    "bank": "bca",
    "installment": {
      "required": false,
      "terms": {
        "bni": [3, 6, 12],
        "mandiri": [3, 6, 12],
        "cimb": [3],
        "bca": [3, 6, 12],
        "offline": [6, 12]
      }
    },
    "whitelist_bins": [
      "48111111",
      "41111111"
    ],
    "dynamic_descriptor": {
      "merchant_name" : "Fuji Apple Inc",
      "city_name": "Jakarta",
      "country_code": "ID"
    }
  },
  "bca_va": {
    "va_number": "12345678911",
    "sub_company_code": "00000",
    "free_text": {
      "inquiry": [
        {
          "en": "text in English",
          "id": "text in Bahasa Indonesia"
        }
      ],
      "payment": [
        {
          "en": "text in English",
          "id": "text in Bahasa Indonesia"
        }
      ]
    }
  },
  "bni_va": {
    "va_number": "12345678"
  },
  "bri_va": {
    "va_number": "1234567891234"
  },
  "cimb_va": {
    "va_number": "1234567891234567"
  },  
  "permata_va": {
    "va_number": "1234567890",
    "recipient_name": "SUDARSONO"
  },
  "shopeepay": {
    "callback_url": "http://shopeepay.com"
  },
  "gopay": {
    "enable_callback": true,
    "callback_url": "http://gopay.com"
  },
  "callbacks": {
    "finish": "https://demo.midtrans.com"
  },
  "uob_ezpay": {
    "callback_url": "http://uobezpay.com"
  }, 
  "expiry": {
    "start_time": "2018-12-13 18:11:08 +0700",
    "unit": "minutes",
    "duration": 1
  },
"page_expiry": {
    "duration": 3,
    "unit": "hours"
},
"recurring": {
    "required": true,
    "start_time": "2024-06-09 15:07:00 +0700",
    "interval_unit": "week"
},  
  "custom_field1": "custom field 1 content",
  "custom_field2": "custom field 2 content",
  "custom_field3": "custom field 3 content"
}
