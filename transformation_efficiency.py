metadata = {"apiLevel": "2.8"}
# Transformation Efficiency (cfu/μg) = (Number of colonies at dilution i) × 2000 × 3ᶦ
# Note: automated transformations ARE much less efficient than reported numbers
# from companies. However, there are reasons behind this:
# 
# 1. Cells tend to be more efficient at transforming lower quantities. Your
#    transformation rate will be greater at 100pg than 1ng. I use a rather
#    large quantity of pUC19 to greater replicate the kind of workflows you'd
#    actually see.
# 2. Outgrowth times double the cells. You don't get pure transformations.
#    If E.coli doubles at 20min, that means you have 8x the transformation
#    after an hour, even if you don't truly have that greater time. For non-amp
#    plasmids, this is necessary, but it does inflate numbers.
# 3. Heat shock cannot be done as effectively in an automated fashion.
#
# Because of these factors, our transformation rates are not directly
# comparable. What this repo mostly tests for is stability of lyophilized
# competent cells over time at different temperatures (20c, 4c, and -20c),
# which is why there are 3 experimental conditions.
#
# The positive control here to test against are NEB's high efficiency turbos.
# NEB is great, and their positive controls are first-rate, so we use them
# as a standard benchmark to test our cells.

experiments = [{
    "origin_location": "temperature_deck",
    "origin_well": "D1",
    "name": "pos ctrl",
    "kcm": False,
    },
    {
    "origin_location": "rack",
    "origin_well": "A1",
    "name": "pos ctrl",
    "kcm": True
    },
    {
    "origin_location": "rack",
    "origin_well": "B1",
    "name": "pos ctrl",
    "kcm": True
    },
         {
    "origin_location": "rack",
    "origin_well": "C1",
    "name": "pos ctrl",
    "kcm": True
    },
]

def run(protocol):
    # Initialize modules and pipettes
    thermocycler_module = protocol.load_module("thermocycler module", 7)  # covers 7,8,9,10
    thermocycler_plate = thermocycler_module.load_labware("nest_96_wellplate_100ul_pcr_full_skirt")
    temperature_module = protocol.load_module("temperature module", 4)
    temperature_deck = temperature_module.load_labware("opentrons_24_aluminumblock_nest_1.5ml_screwcap")  # also used for various reagents
    rack = protocol.load_labware("opentrons_24_tuberack_nest_0.5ml_screwcap", 1)
    agar_plate = protocol.load_labware("biorad_96_wellplate_200ul_pcr", 3)
    p20s = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[protocol.load_labware("opentrons_96_tiprack_20ul", x) for x in [5]])
    p300s = protocol.load_instrument("p300_single_gen2", "left", tip_racks=[protocol.load_labware("opentrons_96_tiprack_300ul", x) for x in [6]])

    # Make deck cold, then load the rest of the reagents
    temperature_module.set_temperature(celsius=10)
    protocol.pause("load reagents")
    thermocycler_module.close_lid()
    thermocycler_module.set_block_temperature(temperature=4)
    thermocycler_module.open_lid()

    water = temperature_deck.wells_by_name()["A1"] # at least 500uL of water. Should be ice cold BEFORE you set it in the 4c.
    kcm = temperature_deck.wells_by_name()["B1"] # 5x concentration
    pUC19 = temperature_deck.wells_by_name()["C1"] # 500pg/uL, at least 30uL
    trash = temperature_deck.wells_by_name()["D1"]
    dilution_water = temperature_deck.wells_by_name()["A2"]
    # The empty tubes start getting placed at A3, but you can place your controls wherever
    open_temperature_wells_addresses = ["{}{}".format(b,a+1) for a in range(2,6) for b in "ABCD" if not any(exp["origin_well"] == "{}{}".format(b,a+1) and exp["origin_location"] == "temperature_deck" for exp in experiments)][1:]
    open_temperature_wells = [temperature_deck.wells_by_name()[x] for x in open_temperature_wells_addresses]

    pos_ctrl = thermocycler_plate.wells_by_name()["A1"]
    neg_ctrl = thermocycler_plate.wells_by_name()["B1"]

    # Here we set up the experimental wells
    # We are meaning to test the transfer from lyophilized containers to cold
    # containers. The idea here is that on a robotic deck you'll have a set of
    # lyophilized reagents, and then you'll move the ones you need to a cold
    # deck. We're building that test into our numbers.
    open_thermocycler_wells = [thermocycler_plate.wells_by_name()[x] for x in ["{}{}".format(b,a+1) for a in range(12) for b in "ABCDEFGH"]]
    pcr_wells = []
    used_temperature_wells = 0
    for i, experiment in enumerate(experiments):
        wells_pair = open_thermocycler_wells[i*2:(i*2)+2]  # Get two wells at a time
        experiment["target_wells"] = experiment.get("target_wells", []) + wells_pair
        if experiment["origin_location"] == "rack":
            experiment["temperature_well"] = open_temperature_wells[used_temperature_wells]
            print("tube in temperature_module {}".format(open_temperature_wells_addresses[used_temperature_wells]))
            used_temperature_wells+=1
        else:
            experiment["temperature_well"] = temperature_deck.wells_by_name()[experiment["origin_well"]]
            print("{} in temperature_module {}".format(experiment["name"], experiment["origin_well"]))

    # Resuspend each experimental lyo tube with 100uL of water
    for experiment in experiments:
        if experiment["origin_location"] != "rack":
            continue
        from_well = rack.wells_by_name()[experiment["origin_well"]]
        to_well = experiment["temperature_well"]
        p300s.pick_up_tip()
        p300s.aspirate(100, water)
        p300s.dispense(100, from_well)
        for _ in range(10):
            p300s.aspirate(60, from_well)
            p300s.dispense(60, from_well.bottom(5))
        p300s.aspirate(100, from_well.bottom(0.5))
        p300s.dispense(100, to_well)
        p300s.drop_tip()

    # Transfer 20ul of pos/neg to pcr machine, starting with control, which goes into
    # A1 and B1 always
    for experiment in experiments:
        p20s.pick_up_tip()
        p20s.aspirate(20, experiment["temperature_well"])
        for well in experiment["target_wells"]:
            p20s.dispense(10, well)
        p20s.drop_tip()

    # Now, add 2uL of pUC19/water to pos/neg, then to experimentals
    for experiment in experiments:
        for i, vec in enumerate([pUC19, water]):
            target = experiment["target_wells"][i]
            p20s.pick_up_tip()
            if experiment["kcm"]:
                p20s.aspirate(4, water)
                p20s.aspirate(4, kcm)
                p20s.aspirate(2, vec)
                p20s.dispense(10, target)
                p20s.mix(4, 6, target)
            if not experiment["kcm"]:
                p20s.aspirate(2, vec)
                p20s.dispense(2, target)
                p20s.mix(4, 6, target)
            p20s.drop_tip()

    # Transform
    temperature_module.deactivate()
    thermocycler_module.close_lid()
    protocol.delay(seconds=1800)  # Wait 30 minutes
    thermocycler_module.set_block_temperature(temperature=42, hold_time_seconds=60)  # heat shock
    thermocycler_module.set_block_temperature(temperature=4, hold_time_minutes=5)
    thermocycler_module.deactivate_block()
    thermocycler_module.deactivate_lid()
    thermocycler_module.open_lid()

    # Plate
    for experiment in experiments: # get vol to 20uL for all
        if not experiment["kcm"]:
            [p20s.transfer(8, water, x, new_tip="always") for x in experiment["target_wells"]]
    dilutions = 4
    for i in range(dilutions): # dilutions
        for j, experiment in enumerate(experiments):
            for k in range(2): # pos, then neg control
                from_well = experiment["target_wells"][k]
                target_well = agar_plate.wells_by_name()["ABCDEFGH"[(j*2)+k] + str(i+1)]
                # The following pattern: A1 (ctrl-pos_ctrl), B1 (ctrl-neg_ctrl), C1 (exp1-pos_ctrl), D1 (exp1-neg_ctrl), E1 (exp2-pos_ctrl) ... 
                p20s.pick_up_tip()
                if i != 0:
                    p20s.aspirate(20, dilution_water)
                    p20s.dispense(20, from_well)
                p20s.mix(2, 5, from_well)
                if i != 0:
                    p20s.aspirate(20, from_well)
                else:
                    p20s.aspirate(10, from_well)
                p20s.move_to(target_well.top(4))
                p20s.dispense(5)
                p20s.move_to(target_well.bottom())
                p20s.move_to(target_well.top())
                p20s.dispense(p20s.current_volume, trash)
                p20s.drop_tip()

