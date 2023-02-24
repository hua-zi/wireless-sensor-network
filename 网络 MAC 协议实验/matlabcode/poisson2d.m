function [ pproc,npoints ] = poisson2d( lambda )
% POISSON2D generate and plot Poisson process in the plane 
%   (square [0,1]x[0,1]). 
% 
% [pproc] = poisson2d(lambda)
%
% Inputs: lambda - intensity of the process
%
% Outputs: pproc - a matrix with 2 columns with coordinates of the
%          points of the process
  % the number of points is Poisson(lambda)-distributed
  npoints = poissrnd(lambda);
  % conditioned that the number of points is N,
  % the points are uniformly distributed
  pproc = rand(npoints, 2);
  % plot the process
  %plot(pproc(:, 1), pproc(:, 2), 'pr')
end