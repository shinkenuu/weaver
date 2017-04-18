select e.vehicle_id, e.schema_id, e.data_value, opt_l.option_id, opt_l.option_code, opt_b.rule_type, opt_b.option_rule
from equipment e
	join option_list opt_l
		on opt_l.vehicle_id = e.vehicle_id
		and opt_l.option_id = e.option_id
	join option_build opt_b
		on opt_b.vehicle_id = e.vehicle_id
		and opt_b.option_id = e.option_id
	where e.schema_id in (
			47002	-- JATO value
			,47102	-- take rate (%)
			,47508	-- deposit (%) | entrada
			,47504	-- 1st period maximum terms (months) | parcelas
			,47505	-- 1st period interest rate | taxa juros
			,45102	-- start date
			,45103	-- end date
			,51208	-- dealer contrib
			,51209	-- manuf contrib
			,51210	-- gov contrib
			,45204	-- public notes
			,45209	-- internal comments
			)
	and (e.[location] = 'BR' OR e.[location] = '-')