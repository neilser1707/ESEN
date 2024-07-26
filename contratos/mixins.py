from datetime import datetime
from .models import ReglasAños, TiposOficios, Descuentos

class Calculos():
    def calcular_años(self, fecha):

        """
            Se encaraga de calcular la diferencia de años entre 2 fechas
            Lo cual se eutiliza para saber las tarifas y descuentos del tomador
        """

        #Fecha inicial
        fecha_inicial = fecha
        dia_inicial = fecha_inicial[4:]
        if int(dia_inicial[0]) == 0:
            dia_inicial = dia_inicial[1]
        mes_inicial = fecha_inicial[2:4]
        if int(mes_inicial[0]) == 0:
            mes_inicial = mes_inicial[1]
        año_inicial = fecha_inicial[:2]
        if int(año_inicial[0]) == 0 or int(año_inicial[0]) == 1 or int(año_inicial[0]) == 2:
            año_inicial = "20" + año_inicial
        else:
            año_inicial = "19" + año_inicial

        #Fecha actual
        fecha_actual = str(datetime.now().date()).replace("-", "")[2:]
        dia = fecha_actual[4:]
        if int(dia[0]) == 0:
            dia = dia[1]
        mes = fecha_actual[2:4]
        if int(mes[0]) == 0:
            mes = mes[1]
        año = "20" + fecha_actual[:2]

        #Analizar y calcular los años de diferencia

        años_dif = int(año) - int(año_inicial)

        if int(mes_inicial) > int(mes):
            años_dif = años_dif - 1
        elif int(mes_inicial) == int(mes):
            if int(dia_inicial) < int(dia):
                años_dif = años_dif - 1
        return años_dif
    
    def clalular_tarifa_muerte(self, contrato):
        
        """
            Mediante "calcular" años obtiene los años del tomador y usando los valores predeterminados
            en la BD se decide su tarifa a pagar
        """

        edad = self.calcular_años(fecha=str(contrato.first().tomadores.tomador.ci)[:6])
        tarifas_edad = ReglasAños.objects.all()
        flag = False
        for tarifa in tarifas_edad:
            rango = tarifa.rango_años
            if edad <= rango:
                flag = True
                break
        if not flag:
            rango = 60
        
        tarifa_muerte = ReglasAños.objects.get(rango_años=rango).porcentaje * contrato.first().valor_muerte
        if contrato.first().periodo_pago == 3:
            tarifa_muerte = tarifa_muerte/4
        elif contrato.first().periodo_pago == 6:
            tarifa_muerte = tarifa_muerte/2
        return tarifa_muerte

    def calcular_tarifa_incapacidad_temporal(self, contrato):

        """
            Dada la información referente al tomador y su grupo ocupacional se le asigna
            Un tarifa correspondiente
        """
        
        tarifa = TiposOficios.objects.get(tipo=contrato.first().tipo_oficio).costo_diario
        if contrato.first().periodo_pago == 3:
            tarifa = tarifa/4
        elif contrato.first().periodo_pago == 6:
            tarifa = tarifa/2
        return contrato.first().valor_incapacidad_temporal * tarifa
    
    def calcular_tarifa_incapacidad_permanete(self, contrato):

        """
            Dada la información referente al tomador y su grupo ocupacional se le asigna
            Un tarifa correspondiente
        """

        tarifa = TiposOficios.objects.get(tipo=contrato.first().tipo_oficio).porcenntaje * contrato.first().valor_incapacidad_permanente
        if contrato.first().periodo_pago == 3:
            tarifa = tarifa/4
        elif contrato.first().periodo_pago == 6:
            tarifa = tarifa/2
        return tarifa

    def calcular_descuentos(self, contrato):

        """
            Mediante "calcular_años" se obtiene la diferencia de años entre el momento en que el
            Tomador se inscribió en dicho contrato y la fecha actual para calcular los descuentos
            Asociados
        """

        fecha_inicio = str(contrato.first().fecha_inicio)[2:10]
        fecha = fecha_inicio.replace('-', '')
        años = self.calcular_años(fecha=fecha)
        descuentos = Descuentos.objects.all()
        flag = False
        for año in descuentos:
            if años == año.años:
                flag = True
                break
        if not flag and años >= 2:
            años = descuentos.last().años
            descuento = Descuentos.objects.get(años=años).porcenntaje*años
        else:
            descuento = 0

        if contrato.first().periodo_pago == 3:
            descuento = descuento/4
        elif contrato.first().periodo_pago == 6:
            descuento = descuento/2
            
        return descuento
        
                

