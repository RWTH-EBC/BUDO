within AixLib.Fluid.BoilerCHP.Examples;
package Test_BUDO
  model boiler
    import AixLib;

    AixLib.Fluid.BoilerCHP.Boiler boiler(redeclare package Medium =
          Modelica.Media.Water.ConstantPropertyLiquidWater,
      paramHC=
          AixLib.DataBase.Boiler.DayNightMode.HeatingCurves_Vitotronic_Day25_Night10(),
      paramBoiler=AixLib.DataBase.Boiler.General.Boiler_Vitogas200F_35kW(),
      TN=5,
      tau=5,
      transferHeat=true,
      tauHeaTra=1800,
      riseTime=60,
      KR=1.00,
      m_flow_nominal=2)                                             "BOI-H02.1"
      annotation (Placement(transformation(extent={{-30,34},{24,90}})));
    Modelica.Fluid.Interfaces.FluidPort_b port_b1(redeclare package Medium =
          Modelica.Media.Water.ConstantPropertyLiquidWater)
      "Fluid connector b (positive design flow direction is from port_a to port_b)"
      annotation (Placement(transformation(extent={{90,50},{116,74}})));
    Modelica.Fluid.Interfaces.FluidPort_a port_a1(redeclare package Medium =
          Modelica.Media.Water.ConstantPropertyLiquidWater)
      "Fluid connector a (positive design flow direction is from port_a to port_b)"
      annotation (Placement(transformation(extent={{-112,50},{-88,74}})));
    Modelica.Blocks.Interfaces.BooleanInput isOn1
      "Switches Controler on and off" annotation (Placement(transformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={28,148})));
    Modelica.Blocks.Interfaces.BooleanInput switchToNightMode1
      "Connector of Boolean input signal" annotation (Placement(transformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={-26,148})));
    Modelica.Blocks.Interfaces.RealInput TAmbient1 "Ambient air temperature"
      annotation (Placement(transformation(
          extent={{-20,-20},{20,20}},
          rotation=90,
          origin={0,148})));
    AixLib.Fluid.Sensors.Temperature temperature_sensor_2(redeclare package
        Medium = Modelica.Media.Water.ConstantPropertyLiquidWater)
      "SEN.T-B06_WS.H.RET.PRIM_MEA.T_AI"
      annotation (Placement(transformation(extent={{42,62},{84,106}})));
    AixLib.Fluid.Sensors.Temperature temperature_sensor_1(redeclare package
        Medium = Modelica.Media.Water.ConstantPropertyLiquidWater)
      "SEN.T-B01_WS.H.SUP.PRIM_MEA.T_AI"
      annotation (Placement(transformation(extent={{-86,62},{-44,106}})));
  equation
    connect(boiler.isOn, isOn1) annotation (Line(points={{10.5,36.8},{28,36.8},
            {28,148}},                 color={255,0,255}));
    connect(boiler.switchToNightMode, switchToNightMode1)
      annotation (Line(points={{-21.9,73.2},{-26,73.2},{-26,148}},
                                                           color={255,0,255}));
    connect(boiler.TAmbient, TAmbient1)
      annotation (Line(points={{-21.9,81.6},{-21.9,148},{0,148}},
                                                        color={0,0,127}));
    connect(port_a1, temperature_sensor_1.port)
      annotation (Line(points={{-100,62},{-65,62}}, color={0,127,255}));
    connect(temperature_sensor_1.port, boiler.port_a)
      annotation (Line(points={{-65,62},{-30,62}}, color={0,127,255}));
    connect(boiler.port_b, port_b1)
      annotation (Line(points={{24,62},{103,62}}, color={0,127,255}));
    connect(boiler.port_b, temperature_sensor_2.port)
      annotation (Line(points={{24,62},{63,62}}, color={0,127,255}));
    annotation (Icon(coordinateSystem(preserveAspectRatio=false, extent={{-100,
              0},{100,120}})),                                     Diagram(
          coordinateSystem(preserveAspectRatio=false, extent={{-100,0},{100,120}})));
  end boiler;

  model CompleteModel
    boiler boiler_system "4120//BOI-H02.1"
      annotation (Placement(transformation(extent={{-26,8},{-6,28}})));
    AixLib.Fluid.Sources.FixedBoundary bou1(nPorts=1, redeclare package Medium =
          Modelica.Media.Water.ConstantPropertyLiquidWater)
      annotation (Placement(transformation(extent={{54,12},{34,32}})));
    Sources.MassFlowSource_T boundary(
      use_m_flow_in=true,
      use_T_in=true,
      nPorts=1,
      redeclare package Medium =
          Modelica.Media.Water.ConstantPropertyLiquidWater)
      annotation (Placement(transformation(extent={{-74,14},{-54,34}})));
    Modelica.Blocks.Sources.CombiTimeTable combiTimeTable(
      smoothness=Modelica.Blocks.Types.Smoothness.ConstantSegments,
      extrapolation=Modelica.Blocks.Types.Extrapolation.HoldLastPoint,
      tableOnFile=true,
      fileName=
          "D:/Sciebo/Programmierung/GIT/_Standard/AixLib/AixLib/Fluid/BoilerCHP/Examples/test_budo_1.mat",
      verboseRead=false,
      tableName="T",
      columns=1:5,
      offset={0,273.15,273.15,0,0})
      annotation (Placement(transformation(extent={{-10,-10},{10,10}},
          rotation=-90,
          origin={-90,90})));

    Modelica.Blocks.Sources.BooleanConstant booleanConstant(k=false)
      annotation (Placement(transformation(extent={{-50,48},{-42,56}})));
    Modelica.Blocks.Sources.Constant const(k=23)
      annotation (Placement(transformation(extent={{-38,68},{-32,74}})));
    Modelica.Blocks.Logical.GreaterEqualThreshold greaterEqualThreshold(threshold=
         0.01)         annotation (Placement(transformation(
          extent={{-5,-5},{5,5}},
          rotation=-90,
          origin={-9,77})));
    inner Modelica.Fluid.System system
      annotation (Placement(transformation(extent={{44,74},{64,94}})));
  equation
    connect(boiler_system.port_b1, bou1.ports[1]) annotation (Line(points={{-5.7,
            18.3333},{4,18.3333},{4,22},{34,22}},
                                            color={0,127,255}));
    connect(boundary.ports[1], boiler_system.port_a1) annotation (Line(points={{-54,24},
            {-26,24},{-26,18.3333}},       color={0,127,255}));
    connect(booleanConstant.y, boiler_system.switchToNightMode1) annotation (
        Line(points={{-41.6,52},{-20,52},{-20,32.6667},{-18.6,32.6667}},
                                                                   color={255,0,
            255}));
    connect(const.y, boiler_system.TAmbient1) annotation (Line(points={{-31.7,
            71},{-31.7,71.5},{-16,71.5},{-16,32.6667}},  color={0,0,127}));
    connect(greaterEqualThreshold.y, boiler_system.isOn1) annotation (Line(
          points={{-9,71.5},{-9,50.75},{-13.2,50.75},{-13.2,32.6667}},
                                                                  color={255,0,
            255}));
    connect(combiTimeTable.y[2], boundary.T_in) annotation (Line(points={{-90,
            79},{-84,79},{-84,28},{-76,28}}, color={0,0,127}));
    connect(combiTimeTable.y[4], boundary.m_flow_in) annotation (Line(points={{
            -90,79},{-82,79},{-82,32},{-74,32}}, color={0,0,127}));
    connect(combiTimeTable.y[5], greaterEqualThreshold.u) annotation (Line(
          points={{-90,79},{-50,79},{-50,83},{-9,83}}, color={0,0,127}));
    annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
          coordinateSystem(preserveAspectRatio=false)));
  end CompleteModel;
  annotation (experiment(StopTime=86400), __Dymola_experimentSetupOutput);
end Test_BUDO;
