# เครื่องวัดชีพจรด้วยแสง Optical Heartbeat Detector — feasibility (python feasibility_check.py) → feasibility.md next to this file
import importlib.util, os
spec = importlib.util.spec_from_file_location('feas', os.path.join(
    os.path.expanduser('~'), '.claude', 'skills', 'fusion-design', 'references', 'feasibility.py'))
feas = importlib.util.module_from_spec(spec); spec.loader.exec_module(feas)
R = feas.Report('เครื่องวัดชีพจรด้วยแสง Optical Heartbeat Detector')
# R.power_budget(12.5, [('name', 12, I_typ, I_stall), ...])
# R.driver_channel('MDD3A ch1', 3, 5, 'motor', run_A, stall_A, 4, 16, 12)
# R.torque('servo', mass_kg, lever_mm, rated_kgcm, stall_kgcm)
# R.beam_udl('frame span', kg, span_mm, n_beams=2)
# R.vessel_box('tank', l_mm, w_mm, h_mm, need_ml)
print(R.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feasibility.md')))
