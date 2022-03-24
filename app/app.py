from tokenize import Double
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)


def solveSimultaneous(a, b, c, d, e, f):
    determinant = (a*e) - (b*d)
    x = round(((e*c)+(-1*b*f))/determinant, 4)
    y = round(((a*f) + (-1 * d*c))/determinant, 4)
    return [x, y]


def resultProducer(p1, c1, p2, c2, b11, b12, b21, b22, pd, accuracy):
    try:
        print("ITERATION ENGINE")
        lmda = p1*(pd/2) + c1
        error = 2
        results = []
        while(error > accuracy):
            payload = {}
            [a, b, c, d, e, f] = [p1*(1+2*lmda*b11), 2*p2*b12*lmda,
                                  lmda-c1, lmda*2*b21*p1, p2*(1+2*b22*lmda), lmda-c2]
            [P1, P2] = solveSimultaneous(a, b, c, d, e, f)
            PL = round(P1*(b11*P1 + b12*P2) + P2*(b21*P1+b22*P2), 4)
            PDPL = round(pd+PL, 4)
            P1P2 = round(P1+P2, 4)
            lmda = lmda + (PDPL-P1P2)
            error = PDPL-P1P2
            payload['Lamda'] = lmda
            payload['P1'] = P1
            payload['P2'] = P2
            payload['Power Loss'] = PL
            payload['P1+P2'] = P1P2
            payload['PD + PL'] = PDPL
            results.append(payload)

        return results
    except:
        return "Please pass all required arguments for optimal dispatch"


dispatch_args = reqparse.RequestParser()
dispatch_args.add_argument(
    "P1", type=float, help="P1 required"
)
dispatch_args.add_argument(
    "C1", type=float, help="C1 required"
)
dispatch_args.add_argument(
    "P2", type=float, help="P2 required"
)
dispatch_args.add_argument(
    "C2", type=float, help="C2 required"
)
dispatch_args.add_argument(
    "B11", type=float, help="B11 required"
)
dispatch_args.add_argument(
    "B12", type=float, help="B12 required"
)
dispatch_args.add_argument(
    "B21", type=float, help="B21 required"
)
dispatch_args.add_argument(
    "B22", type=float, help="B11 required"
)
dispatch_args.add_argument(
    "PD", type=float, help="PD required"
)
dispatch_args.add_argument(
    "ACCURACY", type=float, help="ACCURACY required"
)


class economicDispatch(Resource):

    def get(self):
        args = dispatch_args.parse_args()

        response = {
            "Developer": "Kosgei Victor",
            "email": "victorkosgei254@gmail.com",
            "Title": "Economic Dispatch of Generators",
            "results": resultProducer(args["P1"], args["C1"], args["P2"], args["C2"], args["B11"],
                                      args["B12"], args["B21"], args["B22"], args["PD"], args["ACCURACY"])
        }
        return response


# [a,b,c,d,e,f] = resultProducer(1,200,2,150,0.001,-0.0005,-0.0005,0.0024,100,0.01)
api.add_resource(economicDispatch, "/")
