import chainladder as cl
import pandas as pd
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
import json

app = Flask("Calculation")
CORS(app)
api = Api(app)

class Calculate(Resource):
    def post(self):
        print(request.files)
        raw_data = request.files['files[]'].read()
        raa_df = pd.read_excel(raw_data)
        # print(raa_df.head)
        raa = cl.Triangle(
        raa_df,
        origin="Accident Month",
        development="Report Month",
        columns="Total Loss",
        cumulative=True,
        )
        ratio = raa.link_ratio.to_frame().to_json()
        model = cl.Chainladder().fit(raa)
        ultimates = model.ultimate_.to_frame()  
        a = raa.incr_to_cum().latest_diagonal.sum()
        b = ultimates.sum().values[0]
        ibnr = b - a
        return {"lossTriangle": json.loads(raa.to_frame().to_json()), "ratio":json.loads(ratio), "ibnr":ibnr}


api.add_resource(Calculate, '/')

if __name__ == '__main__':
    app.run()