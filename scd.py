

def sales_fact(schema):
    return f'''
    --Удаление из фактовой таблицы заказы которые есть в стейджинг
    delete from {schema}.fact_sales
    where srid in (
	select srid
	from {schema}.stg_sales stg
);
    
    insert into {schema}.fact_sales(date, lastChangeDate, supplierArticle, techSize, barcode, totalPrice,
	discountPercent, isSupply, isRealization, promoCodeDiscount, warehouseName, countryName, oblastOkrugName,
	regionName, incomeID, saleID, odid, spp, forPay, finishedPrice, priceWithDisc, nmId, subject, category, brand,
	IsStorno, gNumber, sticker, srid)
    select
	stg.date,
	stg.lastChangeDate,
	stg.supplierArticle,
	stg.techSize,
	stg.barcode,
	stg.totalPrice,
	stg.discountPercent,
	stg.isSupply,
	stg.isRealization,
	stg.promoCodeDiscount,
	stg.warehouseName,
	stg.countryName,
	stg.oblastOkrugName,
	stg.regionName,
	stg.incomeID,
	stg.saleID,
	stg.odid,
	stg.spp,
	stg.forPay,
	stg.finishedPrice,
	stg.priceWithDisc,
	stg.nmId,
	stg.subject,
	stg.category,
	stg.brand,
	stg.IsStorno,
	stg.gNumber,
	stg.sticker,
	stg.srid
from {schema}.stg_sales stg'''


def orders_fact(schema):
    return f'''
--Удаление из фактовой таблицы заказы которые есть в стейджинг
delete from {schema}.fact_orders
where srid in (
	select srid
	from {schema}.stg_orders
);



--Загружаем заказы из стейджинга
insert into {schema}.fact_orders (date, lastChangeDate, supplierArticle, techSize, barcode, totalPrice, 
discountPercent, warehouseName, oblast, incomeID, odid, nmId, subject, category, brand, isCancel, cancel_dt, 
gNumber, sticker, srid)
select 
stg.date, 
stg.lastChangeDate, 
stg.supplierArticle, 
stg.techSize, 
stg.barcode, 
stg.totalPrice, 
stg.discountPercent, 
stg.warehouseName, 
stg.oblast, 
stg.incomeID, 
stg.odid, 
stg.nmId, 
stg.subject, 
stg.category, 
stg.brand, 
stg.isCancel, 
stg.cancel_dt, 
stg.gNumber, 
stg.sticker, 
stg.srid
from {schema}.stg_orders stg
'''


def stocks_fact(schema):
    return f'''insert into {schema}.fact_stocks(reportbydate, lastChangeDate, supplierArticle, techSize, barcode, quantity, 
isSupply, isRealization, quantityFull, warehouseName, nmId, subject, category, daysOnSite, brand, SCCode, 
Price, Discount)
select
Date(now()),
stg.lastChangeDate, 
stg.supplierArticle, 
stg.techSize, 
stg.barcode, 
stg.quantity, 
stg.isSupply, 
stg.isRealization, 
stg.quantityFull, 
stg.warehouseName, 
stg.nmId, 
stg.subject, 
stg.category, 
stg.daysOnSite, 
stg.brand, 
stg.SCCode, 
stg.Price, 
stg.Discount
from {schema}.stg_stocks stg
where Date(now()) > coalesce((select max(reportbydate) from {schema}.fact_stocks), Date(now()) - integer '1')
'''


def fact_incomes(schema):
    return f'''insert into {schema}.fact_incomes (incomeId, number, date, lastChangeDate, supplierArticle, 
techSize, barcode, quantity, totalPrice, dateClose, warehouseName, nmId, status)
select 
stg.incomeId, 
stg.number, 
stg.date, 
stg.lastChangeDate, 
stg.supplierArticle, 
stg.techSize, 
stg.barcode, 
stg.quantity, 
stg.totalPrice, 
stg.dateClose, 
stg.warehouseName, 
stg.nmId, 
stg.status
from {schema}.stg_incomes stg
left join {schema}.fact_incomes tgt
on stg.incomeid = tgt.incomeid and stg.barcode = tgt.barcode and stg.nmid = tgt.nmid 
where 1 = 0
or stg.incomeid <> tgt.incomeid or ( stg.incomeid is null and tgt.incomeid is not null ) or ( stg.incomeid is not null and tgt.incomeid is null )
or stg.barcode <> tgt.barcode or ( stg.barcode is null and tgt.barcode is not null ) or ( stg.barcode is not null and tgt.barcode is null )
or stg.nmid <> tgt.nmid or ( stg.nmid is null and tgt.nmid is not null ) or ( stg.nmid is not null and tgt.nmid is null )
'''


def fact_report_week(schema):
    return f'''insert into {schema}.fact_reportdetailbyperiod (realizationreport_id, date_from, date_to, create_dt, 
suppliercontract_code, rrd_id, gi_id, subject_name, nm_id, brand_name, sa_name, ts_name, barcode, doc_type_name,
quantity, retail_price, retail_amount, sale_percent, commission_percent, office_name, supplier_oper_name, order_dt,
sale_dt, rr_dt, shk_id, retail_price_withdisc_rub, delivery_amount, return_amount, delivery_rub, gi_box_type_name,
product_discount_for_report, supplier_promo, rid, ppvz_spp_prc, ppvz_kvw_prc_base, ppvz_kvw_prc, 
ppvz_sales_commission, ppvz_for_pay, ppvz_reward, acquiring_fee, acquiring_bank, ppvz_vw, ppvz_vw_nds, 
ppvz_office_id, ppvz_office_name, ppvz_supplier_id, ppvz_supplier_name, 
ppvz_inn, declaration_number, sticker_id, site_country, penalty, additional_payment, srid)
select
stg.realizationreport_id, 
stg.date_from, 
stg.date_to, 
stg.create_dt, 
stg.suppliercontract_code, 
stg.rrd_id, 
stg.gi_id, 
stg.subject_name, 
stg.nm_id, 
stg.brand_name, 
stg.sa_name, 
stg.ts_name, 
stg.barcode, 
stg.doc_type_name, 
stg.quantity, 
stg.retail_price, 
stg.retail_amount, 
stg.sale_percent, 
stg.commission_percent, 
stg.office_name, 
stg.supplier_oper_name, 
stg.order_dt, 
stg.sale_dt, 
stg.rr_dt, 
stg.shk_id, 
stg.retail_price_withdisc_rub, 
stg.delivery_amount, 
stg.return_amount, 
stg.delivery_rub, 
stg.gi_box_type_name, 
stg.product_discount_for_report, 
stg.supplier_promo, 
stg.rid, 
stg.ppvz_spp_prc, 
stg.ppvz_kvw_prc_base, 
stg.ppvz_kvw_prc, 
stg.ppvz_sales_commission, 
stg.ppvz_for_pay, 
stg.ppvz_reward, 
stg.acquiring_fee, 
stg.acquiring_bank, 
stg.ppvz_vw, 
stg.ppvz_vw_nds, 
stg.ppvz_office_id, 
stg.ppvz_office_name, 
stg.ppvz_supplier_id, 
stg.ppvz_supplier_name, 
stg.ppvz_inn, 
stg.declaration_number, 
stg.sticker_id, 
stg.site_country, 
stg.penalty, 
stg.additional_payment, 
stg.srid
from {schema}.stg_reportdetailbyperiod stg
left join {schema}.fact_reportdetailbyperiod tgt
on 1 = 1
and stg.realizationreport_id = tgt.realizationreport_id
and stg.rrd_id = tgt.rrd_id
and stg.gi_id = tgt.gi_id
and stg.nm_id = tgt.nm_id
and stg.shk_id = tgt.shk_id
and stg.rid = tgt.rid
and stg.srid = tgt.srid
and stg.supplier_oper_name = tgt.supplier_oper_name
where 1 = 0
or stg.realizationreport_id <> tgt.realizationreport_id or ( stg.realizationreport_id is null and tgt.realizationreport_id is not null ) or ( stg.realizationreport_id is not null and tgt.realizationreport_id is null )
or stg.rrd_id <> tgt.rrd_id or ( stg.rrd_id is null and tgt.rrd_id is not null ) or ( stg.rrd_id is not null and tgt.rrd_id is null )
or stg.gi_id <> tgt.gi_id or ( stg.gi_id is null and tgt.gi_id is not null ) or ( stg.gi_id is not null and tgt.gi_id is null )
or stg.nm_id <> tgt.nm_id or ( stg.nm_id is null and tgt.nm_id is not null ) or ( stg.nm_id is not null and tgt.nm_id is null )
or stg.shk_id <> tgt.shk_id or ( stg.shk_id is null and tgt.shk_id is not null ) or ( stg.shk_id is not null and tgt.shk_id is null )
or stg.rid <> tgt.rid or ( stg.rid is null and tgt.rid is not null ) or ( stg.rid is not null and tgt.rid is null )
or stg.srid <> tgt.srid or ( stg.srid is null and tgt.srid is not null ) or ( stg.srid is not null and tgt.srid is null )
or stg.supplier_oper_name <> tgt.supplier_oper_name or ( stg.supplier_oper_name is null and tgt.supplier_oper_name is not null ) or ( stg.supplier_oper_name is not null and tgt.supplier_oper_name is null )
'''


