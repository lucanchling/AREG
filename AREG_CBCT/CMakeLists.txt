#-----------------------------------------------------------------------------
set(MODULE_NAME AREG_CBCT)

set(MODULE_PYTHON_SCRIPTS 
  ${MODULE_NAME}.py)

SlicerMacroBuildScriptedCLI(
  NAME ${MODULE_NAME}
  RESOURCES ${MODULE_PYTHON_SCRIPTS}
  
  )